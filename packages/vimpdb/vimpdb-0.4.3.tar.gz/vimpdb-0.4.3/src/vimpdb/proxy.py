import os
import sys
import socket

from subprocess import call
from subprocess import Popen
from subprocess import PIPE

from vimpdb.config import CLIENT
from vimpdb.config import logger


def getPackagePath(instance):
    module = sys.modules[instance.__module__]
    return os.path.dirname(module.__file__)


class ProxyToVim(object):
    """
    use subprocess to launch Vim instance that use clientserver mode
    to communicate with Vim instance used for debugging.
    """

    def __init__(self, config):
        self.vim_client_script = config.scripts[CLIENT]
        self.server_name = config.server_name

    def _remote_expr(self, expr):
        p = Popen([self.vim_client_script, '--servername',
                   self.server_name, "--remote-expr", expr],
            stdin=PIPE, stdout=PIPE)
        return_code = p.wait()
        if return_code:
            raise RemoteUnavailable()
        child_stdout = p.stdout
        output = child_stdout.read()
        return output.strip()

    def _send(self, command):
        return_code = call([self.vim_client_script, '--servername',
            self.server_name, '--remote-send', command])
        if return_code:
            raise RemoteUnavailable()
        logger.debug("sent: %s" % command)

    def setupRemote(self):
        if not self.isRemoteSetup():
            package_path = getPackagePath(self)
            filename = os.path.join(package_path, "vimpdb.vim")
            command = "<C-\><C-N>:source %s<CR>" % filename
            self._send(command)
            egg_path = os.path.dirname(package_path)
            self._send(':call PDB_setup_egg(%s)<CR>' % repr(egg_path))

    def isRemoteSetup(self):
        status = self._expr("exists('*PDB_setup_egg')")
        return status == '1'

    def showFeedback(self, feedback):
        if not feedback:
            return
        feedback_list = feedback.splitlines()
        self.setupRemote()
        self._send(':call PDB_show_feedback(%s)<CR>' % repr(feedback_list))

    def showFileAtLine(self, filename, lineno):
        if os.path.exists(filename):
            self._showFileAtLine(filename, lineno)

    def _showFileAtLine(self, filename, lineno):
        # Windows compatibility:
        # Windows command-line does not play well with backslash in filename.
        # So turn backslash to slash; Vim knows how to translate them back.
        filename = filename.replace('\\', '/')
        self.setupRemote()
        self._send(':call PDB_show_file_at_line("%s", "%d")<CR>'
            % (filename, lineno))

    # code leftover from hacking
    def getText(self, prompt):
        self.setupRemote()
        command = self._expr('PDB_get_command("%s")' % prompt)
        return command

    def _expr(self, expr):
        logger.debug("expr: %s" % expr)
        result = self._remote_expr(expr)
        logger.debug("result: %s" % result)
        return result


class ProxyFromVim(object):

    BUFLEN = 512

    def __init__(self, config):
        self.socket_inactive = True
        self.port = config.port

    def bindSocket(self):
        if self.socket_inactive:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                socket.IPPROTO_UDP)
            self.socket.bind(('', self.port))
            self.socket_inactive = False

    def closeSocket(self):
        self.socket.close()
        self.socket_inactive = True

    def waitFor(self, pdb):
        self.bindSocket()
        (message, address) = self.socket.recvfrom(self.BUFLEN)
        logger.debug("command: %s" % message)
        return message


class RemoteUnavailable(Exception):
    pass


# code leftover from hacking
def eat_stdin(self):
    sys.stdout.write('-- Type Ctrl-D to continue --\n')
    sys.stdout.flush()
    sys.stdin.readlines()
