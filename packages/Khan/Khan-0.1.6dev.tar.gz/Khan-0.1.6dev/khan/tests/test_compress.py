# -*- coding: utf-8 -*-

import slimmer
from khan.utils.testing import *
from khan.compress import *

class TestWebMinifier(TestCase):

    js_body = """
    var a = 1;
    // comments
    var b = 2;
    """
    
    js_minified_body = slimmer.js_slimmer(js_body)
    
    css_body = """
    /* comments */
    .a {
    }
    """
    
    css_minified_body = slimmer.css_slimmer(css_body)
    
    html_body = """
    <html>
    <!-- comments -->
    </html>
    """
    
    html_minified_body = slimmer.html_slimmer(html_body)
    
    def js_app(self, environ, start_response):
        start_response("200 OK" , [("Content-Type", "application/x-javascript")])
        return [self.js_body]  
    
    def css_app(self, environ, start_response):
        start_response("200 OK" , [("Content-Type", "text/css")])
        return [self.css_body]  
    
    def html_app(self, environ, start_response):
        start_response("200 OK" , [("Content-Type", "text/html")])
        return [self.html_body]  
    
    def nomatched_app(self, environ, start_response):
        start_response("200 OK" , [("Content-Type", "application/x")])
        return ["nomatched"]  
    
    def test_basic(self):
        nomatched_app = TestApp(WebMinifier(self.nomatched_app))
        resp = nomatched_app.get("/")
        self.assertEqual(resp.body, "nomatched")
        js_app = TestApp(WebMinifier(self.js_app, catch_status = [300]))
        resp = js_app.get("/")
        self.assertEqual(resp.body, self.js_body)
        
    def test_slimmer_plugin(self):
        js_app = TestApp(WebMinifier(self.js_app))
        css_app = TestApp(WebMinifier(self.css_app))
        html_app = TestApp(WebMinifier(self.html_app))
        resp = js_app.get("/")
        self.assertEqual(resp.body, self.js_minified_body)
        resp = css_app.get("/")
        self.assertEqual(resp.body, self.css_minified_body)
        resp = html_app.get("/")
        self.assertEqual(resp.body, self.html_minified_body)
        
if __name__ == "__main__":
    unittest.main()
    