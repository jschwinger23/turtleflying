import socket
from .wait import wait


def get_socket(
    family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None
):
    sock = socket._o_socket(family, type, proto, fileno)
    if (
        family in {socket.AF_INET, socket.AF_INET6} and
        type in {socket.SOCK_DGRAM}
    ):
        return GreenSocket(sock)
    return sock


class GreenSocket:

    def __init__(self, sock):
        self.sock = sock
        self.sock.setblocking(False)

    def recvfrom(self, bufsize, flags=None):
        while True:
            try:
                bytes, address = self.sock.recvfrom(bufsize, flags)
            except BlockingIOError:
                wait(on_readable=self._fileno)
            else:
                return bytes, address

    def sendto(self, bytes, address) -> int:
        while True:
            try:
                sent = self.sock.sendto(bytes, address)
            except BlockingIOError:
                wait(on_writable=self._fileno)
            else:
                return sent

    def __getattr__(self, attr):
        return getattr(self.sock, attr)
