"""An HTTPS connection implementation that does not:

    * depend on swig
    * ignore server certificates

$Id: __init__.py 110605 2010-04-07 18:36:54Z zvezdan $
"""
import socket
import httplib
import ssl
import os.path
import sys


class HTTPSConnection(httplib.HTTPSConnection):
    """An HTTPS connection using the ssl module"""

    def __init__(self, host, port=None, key_file=None, cert_file=None,
                 strict=None, timeout=None):
        if sys.version_info < (2, 6, 0):
            # timeout is None or float
            self.timeout = timeout
            httplib.HTTPSConnection.__init__(
                self, host, port, key_file, cert_file, strict)
        else:
            httplib.HTTPSConnection.__init__(
                self, host, port, key_file, cert_file, strict, timeout)

        if self.cert_file is None:
            self.cert_file = os.path.join(os.path.dirname(__file__),
                                          "certs.pem")

    ssl_wrap_socket = staticmethod(ssl.wrap_socket)

    def connect(self):
        "Connect to a host on a given (SSL) port."
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = self.ssl_wrap_socket(sock,
                                         ca_certs=self.cert_file,
                                         cert_reqs=ssl.CERT_REQUIRED)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
