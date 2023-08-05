# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
version = open(os.path.join(here, 'VERSION.txt')).readline().rstrip()

setup(
    name="Khan",
    version=version,
    description="",
    long_description=README + "\n\n" +  CHANGES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="timbaby2008",
    author_email="timbaby2008@gmail.com",
    url="http://bitbucket.org/khan/khan",
    keywords="web wsgi khan framework",
    install_requires=[
        "setuptools>=0.6c11",
        "babel",
        "Paste",
        "PasteDeploy",
        "PasteScript",
        "tempita",
        "webob",
        "webtest",
        "enum",
        "shove",
        "slimmer",
        "configobj",
        "httplib2",
        "zope.interface",
        "zope.component",
        "zope.schema",
        "zope.deprecation",
        "repoze.zcml",
        "repoze.who==2.0a2",
        "repoze.what==1.0.8",
        "simplejson"
    ],
    tests_require=["nose>=0.11"],
    namespace_packages=['khan'],
    packages=find_packages(exclude=['tests']),
    package_data={
        '': ['CHANGES.txt', 'TODO.txt', 'README.txt', 'VERSION.txt'],
        'docs': ['Makefile', 'source/*'],
        'locals' : ['locales/*/LC_MESSAGES/*.mo']},
    exclude_package_data={'': ['CHANGES.txt', 'TODO.txt', 'README.txt', 'docs']},
    message_extractors={'khan': [('**.py', 'python', None)]},
    include_package_data=True,
    zip_safe=False,
    test_suite="nose.collector",
    entry_points={
        "paste.app_factory" : [
            "status = khan.httpstatus:make_httpstatus_app",
            "jsonpproxy = khan.jsonp:make_jsonp_app",
            "jsonrpc = khan.jsonp:make_jsonrpc_app",
            "static = khan.static:make_static_app",
            "file = khan.static:make_file_app",
            "eventagent = khan.notification:make_httpbasedeventagent_app",
            "rpcstore = khan.store:make_rpcstore_app",
            "proxy = khan.proxy:make_proxy_app",
            "transparent_proxy = khan.proxy:make_transparent_proxy_app",
            "traverser = khan.traversal:make_traverser_app"
        ],
        "paste.composite_factory" :[
             "virtualhost = khan.virtualhost:make_virtualhost_app",
             "ruledispatcher = khan.urlparse:make_ruledispatcher_app",
        ],
        "paste.filter_factory" : [
            "environloadable = khan.deploy.core:make_environloadable_middleware",
            "jsonp = khan.json:make_jsonp_middleware",
            "statusdispatcher = khan.httpstatus:make_httpstatusdispatcher_middleware",
            "urlrestrictor = khan.security.restrict:make_urlrestrictor_middleware",
            "urldecryptor = khan.urlparse:make_urldecryptor_middleware",
            "session = khan.session:make_session_middleware",
            "cache = khan.cache:make_cache_middleware",
            "cached = khan.cache:make_cached_middleware",
            "auth = khan.security.auth:make_auth_middleware",
            "protector = khan.security.auth:make_protector_middleware",
            "frequency_restrictor = khan.security.restrict:make_request_frequency_restrictor_middleware",
            "error_document = khan.error_document:make_error_document_middleware",
            "filterdispatcher = khan.urlparse:make_filterdispatcher_middleware",
            "minifier = khan.compress:make_webminifier_middleware"
        ],
        "khan.loadable_objects" : [
            "dict = khan.deploy.core:make_dict_object",
            "store = khan.store:make_store_object",
            "session.cookie = khan.session:make_cookie_identifier_plugin",
            "session.header = khan.session:make_httpheader_identifier_plugin",
            "session.req_param = khan.session:make_request_param_identifier_plugin",
            "auth.auth_tkt = khan.security.auth:make_authtkt_object",
            "auth.session = khan.security.auth:make_sessionidentifier_object",
            "auth.basicauth = khan.security.auth:make_basicauth_object",
            "auth.form = khan.security.auth:make_form_object",
            "auth.redirecting_form = khan.security.auth:make_redirecting_form_object",
            "auth.htpasswd = khan.security.auth:make_htpasswd_object",
            "auth.store_based_authenticator = khan.security.auth:make_storebasedauthenticator_object",
            "auth.store_based_mdprovider = khan.security.auth:make_storebasemetadataprovider_object",
            "auth.store_based_grpadapter = khan.security.auth:make_store_based_group_adapter",
            "auth.store_based_pemadapter = khan.security.auth:make_store_based_permission_adapter",
            "jsonrpc.client = khan.json:make_jsonrpc_client_object",
            "subscriber.callable = khan.notification:make_callable_subscriber_object",
            "subscriber.command = khan.notification:make_command_subscriber_object",
            "subscriber.http = khan.notification:make_http_subscriber_object",
            "httpsender = khan.notification:make_httpsender_object",
            "subscribed = khan.notification:make_subscribed_object",
        ],
        "shove.stores" : [
            "khan.rpc = khan.store:RPCStore",
            "khan.ini = khan.store:INIStore",
            "khan.dbm = khan.store:KhanDBMStore"
        ],
        "paste.paster_create_template" : [
            "khan.starter = khan.project.starter:StarterTemplate",
            "khan.webpy = khan.project.webpy:WebpyTemplate",
            "khan.django = khan.project.django:DjangoTemplate"
        ],
        "paste.global_paster_command" : [
            "khan.jsonrpc = khan.json:JSONRPCClientCommand",
            "khan.static = khan.static:StaticCommand",
            "khan.serve = khan.scripts.serve:ServeCommand",
            "khan.shell = khan.scripts.shell:ShellCommand",
        ],
        "nose.plugins" : [
            "khan = khan.utils.testing:KhanForNose"
        ]
        
    }
)
