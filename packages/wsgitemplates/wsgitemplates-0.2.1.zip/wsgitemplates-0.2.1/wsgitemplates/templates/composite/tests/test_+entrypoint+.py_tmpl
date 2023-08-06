import unittest
from WebOb import Request

from ${egg}.${entrypointname} import ${entrypointname.title()}Composite

def helloworld(environ, start_response):
    status = "200 OK"
    headers = {'Content-type':'text/plain'}
    start_response(status, headers.items())
    return ("Hello world")

def htmlworld(environ, start_response):
    status = "200 OK"
    headers = {'Content-type':'application/xhtml+xml'}
    start_response(status, headers.items())
    return ("<html><body><h1>Hello world</h1></body></html>")

class test_${entrypointname.lower()}(unittest.TestCase):
    
    def setUp(self):
        super(self.__class__, self).setUp()
        self.app = ${entrypointname.title()}Composite(plain=helloworld, html=htmlworld, default=helloworld)
    
    def test_plain_directory_uses_plain_text(self):
        req = Request.blank('/plain/')
        status, headers, body = req.call_application(self.app)

        # Use more convenient data types
        status = int(status[:3])
        body = ''.join(list(body))
        headers = dict(headers)
        
        assert status == 200
        assert headers['Content-type'] == 'text/plain'
        assert body == "Hello world"

    def test_html_uses_xhtml(self):
        req = Request.blank('/html/')
        status, headers, body = req.call_application(self.app)

        # Use more convenient data types
        status = int(status[:3])
        body = ''.join(list(body))
        headers = dict(headers)
        
        assert status == 200
        assert headers['Content-type'] == 'application/xhtml+xml'
        assert "Hello world" in body

    def test_root_uses_default(self):
        req = Request.blank('/')
        status, headers, body = req.call_application(self.app)

        # Use more convenient data types
        status = int(status[:3])
        body = ''.join(list(body))
        headers = dict(headers)
        
        assert status == 200
        assert headers['Content-type'] == 'application/xhtml+xml'
        assert "Hello world" in body

        
        
