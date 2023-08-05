# -*- coding: utf-8 -*-

import os, unittest
from khan.utils.testing import TestCase, TestApp
from tempfile import mktemp
from khan.static import *

class FileTester(TestCase):
    
    def test_basic(self):
        filename = mktemp()
        fobj = file(filename, "w")
        fobj.close()
        headers = [("X-KK", "kk")]
        content_type = "text/test"
        app = File(filename, headers = headers, content_type = content_type)
        app = TestApp(app)
        resp = app.get("/", status = "*")
        assert resp.content_type == content_type
        assert "X-KK" in resp.headers
        if os.path.isfile(filename):
            os.remove(filename)

if __name__ == "__main__":
    unittest.main()
