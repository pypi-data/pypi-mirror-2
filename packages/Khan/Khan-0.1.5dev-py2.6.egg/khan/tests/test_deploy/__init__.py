#-*- coding: utf-8 -*-

import logging
import os, shutil, glob, time
from tempfile import mkdtemp
from cStringIO import StringIO
from khan.utils.testing import *
from khan.deploy import *
from khan.deploy.core import get_context_from_zcml, make_server_from_sfactory, logging_from_zcml_context
logger = logging.getLogger('root')

def make_composite_a(loader, global_conf, **params):
    obja = global_conf["loader"].get_object("obj_a")
    def composite_app(environ, start_response):
        return []
    return composite_app
    
def make_object_a(global_conf, **params):
    app = global_conf["loader"].get_app("obj_b")
    def obja():
        pass
    return obja

def make_middleware_a(global_conf, **params):
    def filter(app):
        def mapp(environ, start_response):
            return []
        return mapp
    return filter

def make_app_a(global_conf, **params):
    def app(environ, start_response):
        return []
    return app
            
def test_run_server_from_zcml():
    deploy_ctx = get_context_from_zcml("khan.tests.test_deploy")
    server_runner = make_server_from_sfactory(deploy_ctx, "main")
    logging_from_zcml_context(deploy_ctx)
    assert callable(server_runner)
    
if __name__ == "__main__":
    unittest.main()
