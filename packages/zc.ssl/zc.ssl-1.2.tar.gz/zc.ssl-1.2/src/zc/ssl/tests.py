"""Tests for zc.ssl

$Id: tests.py 81831 2007-11-14 13:19:41Z alga $
"""
import unittest
import zope.testing.doctest


class StubSSLWrapper(object):

    def __init__(self, sock, ca_certs=None, cert_reqs=None):
        self.sock = sock
        self.ca_certs = ca_certs
        self.cert_reqs = cert_reqs
        print "sssl(%r, %r, %r)" % (sock, ca_certs, cert_reqs)

    def settimeout(self, timeout):
        print "sssl.settimeout(%r)" % timeout

    def connect(self, hostport):
        print "sssl.connect(%r)" % (hostport, )


def test_suite():
    suite = unittest.TestSuite([
        zope.testing.doctest.DocFileSuite(
        'tests.txt',
        optionflags=zope.testing.doctest.ELLIPSIS),
        ])

    return suite
