import unittest
from urllib import quote_plus

from Products.jsonserver.minjson import write
from Products.jsonserver.interfaces import IJsonRequest

from Products.jsonserver.jsonrpc import patch_HTTPRequest
patch_HTTPRequest()

class PublisherTests( unittest.TestCase ):

    def _getTargetClass(self):
        from ZPublisher.HTTPRequest import HTTPRequest
        return HTTPRequest

    def _makeOne(self, stdin=None, environ=None, clean=1):

        if stdin is None:
            from cStringIO import StringIO
            stdin = StringIO('{ "method": "echo", "params": ["Hello JSON-RPC"], "id": 1}')

        if environ is None:
            environ = {}

        if 'SERVER_NAME' not in environ:
            environ['SERVER_NAME'] = 'http://localhost'

        if 'SERVER_PORT' not in environ:
            environ['SERVER_PORT'] = '8080'

        if 'REQUEST_METHOD' not in environ:
            environ['REQUEST_METHOD'] = 'POST'

        if 'CONTENT_TYPE' not in environ:
            environ['CONTENT_TYPE'] = 'application/json'

        class _FauxResponse(object):
            _auth = None
            _encode_unicode = None
            headers = {}

            def setHeader(self, key, value):
                self.headers[key] = value

            def setBody(self, body):
                self.body = body

            def setStatus(self, status):
                self.status = status

        response = _FauxResponse()
        req = self._getTargetClass()(stdin, environ, response, clean)
        req.processInputs()
        return req

    def test_marker(self):
        req = self._makeOne()
        self.failUnless(IJsonRequest.providedBy(req))

    def test_jsonid(self):
        req = self._makeOne()
        self.assertEqual(req.response._jsonID, 1)

    def test_body(self):
        req = self._makeOne()
        resp = req.response
        resp.setBody('Hello JSON-RPC')
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.body, '{"id":1,"result":"Hello JSON-RPC"}')
        self.assertEqual(resp.headers,
                         {'content-type': 'application/json;charset=utf-8'})

    def test_get(self):
        req = self._makeOne(environ={'REQUEST_METHOD':'GET'})
        resp = req.response
        self.failIf(hasattr(resp, '_jsonID'))

    def test_wrongmimetype(self):
        req = self._makeOne(environ={'CONTENT_TYPE':'text/html'})
        resp = req.response
        self.failIf(hasattr(resp, '_jsonID'))

    def test_alternatemimetype(self):
        req = self._makeOne(environ={'CONTENT_TYPE':'application/json-rpc'})
        resp = req.response
        self.assertEqual(req.response._jsonID, 1)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PublisherTests))
    return suite

