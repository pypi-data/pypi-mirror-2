# -*- coding: utf-8 -*-

"""
URL 分发和过滤
=================================

本模块提供工具去处理 URL 分发和基于正则表达式的 URL 过滤.

索引
=================================

* :func:`urlquote`
* :func:`urlencode`
* :func:`quote_plus`
* :func:`urlsearch`
* :func:`domainsearch`
* :func:`get_wild_domain`
* :func:`remove_port_from_domain`
* :func:`fmt_url`
* :func:`urlencrypt`
* :func:`urldecrypt`
* :func:`make_urldecryptor_middleware`
* :func:`make_ruledispatcher_app`
* :func:`make_filterdispatcher_middleware`

* :class:`RuleDispatcher`
* :class:`URLDecryptor`
* :class:`FilterDispatcher`

=================================

.. autofunction:: urlquote
.. autofunction:: urlencode
.. autofunction:: quote_plus
.. autofunction:: urlsearch
.. autofunction:: domainsearch
.. autofunction:: get_wild_domain
.. autofunction:: remove_port_from_domain
.. autofunction:: fmt_url
.. autofunction:: urlencrypt
.. autofunction:: urldecrypt
.. autofunction:: make_urldecryptor_middleware
.. autofunction:: make_ruledispatcher_app
.. autofunction:: make_filterdispatcher_middleware

.. autoclass:: RuleDispatcher
.. autoclass:: URLDecryptor
.. autoclass:: FilterDispatcher
"""

import os, logging, re
from UserDict import DictMixin
from khan.httpstatus import HTTPStatus
from khan.utils.encryption import Vignere
from khan.utils import get_request_handler_name
from khan.deploy import loadapp, loadfilter

__all__ = [
    "urlsearch",
    "domainsearch",
    "urlencode",
    "urlquote",
    "urlencrypt", 
    "urldecrypt", 
    "RuleDispatcher", 
    "FilterDispatcher",
    "URLDecryptor"
]

always_safe = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '_.-')
_safemaps = {}
_must_quote = {}

def urlquote(s, safe=''):
    """
    拷贝从 ``repoze.bfg`` <http://bfg.repoze.org>_
    
    this function copy from repoze.bfg <http://bfg.repoze.org>_
    
    quote('abc def') -> 'abc%20def'

    Faster version of Python stdlib urllib.quote which also quotes
    the '/' character.  

    Each part of a URL, e.g. the path info, the query, etc., has a
    different set of reserved characters that must be quoted.

    RFC 2396 Uniform Resource Identifiers (URI): Generic Syntax lists
    the following reserved characters.

    reserved    = ";" | "/" | "?" | ":" | "@" | "&" | "=" | "+" |
                  "$" | ","

    Each of these characters is reserved in some component of a URL,
    but not necessarily in all of them.

    Unlike the default version of this function in the Python stdlib,
    by default, the quote function is intended for quoting individual
    path segments instead of an already composed path that might have
    '/' characters in it.  Thus, it *will* encode any '/' character it
    finds in a string.
    """
    
    cachekey = (safe, always_safe)
    try:
        safe_map = _safemaps[cachekey]
        if not _must_quote[cachekey].search(s):
            return s
    except KeyError:
        safe += always_safe
        _must_quote[cachekey] = re.compile(r'[^%s]' % safe)
        safe_map = {}
        for i in range(256):
            c = chr(i)
            safe_map[c] = (c in safe) and c or ('%%%02X' % i)
        _safemaps[cachekey] = safe_map
    res = map(safe_map.__getitem__, s)
    return ''.join(res)

def urlencode(query, doseq=True):
    """
    拷贝从 ``repoze.bfg`` <http://bfg.repoze.org>_
    
    An alternate implementation of Python's stdlib `urllib.urlencode
    function <http://docs.python.org/library/urllib.html>`_ which
    accepts unicode keys and values within the ``query``
    dict/sequence; all Unicode keys and values are first converted to
    UTF-8 before being used to compose the query string.

    The value of ``query`` must be a sequence of two-tuples
    representing key/value pairs *or* an object (often a dictionary)
    with an ``.items()`` method that returns a sequence of two-tuples
    representing key/value pairs.

    For minimal calling convention backwards compatibility, this
    version of urlencode accepts *but ignores* a second argument
    conventionally named ``doseq``.  The Python stdlib version behaves
    differently when ``doseq`` is False and when a sequence is
    presented as one of the values.  This version always behaves in
    the ``doseq=True`` mode, no matter what the value of the second
    argument.

    See the Python stdlib documentation for ``urllib.urlencode`` for
    more information.
    """
    
    try:
        # presumed to be a dictionary
        query = query.items()
    except AttributeError:
        pass

    result = ''
    prefix = ''

    for (k, v) in query:
        if k.__class__ is unicode:
            k = k.encode('utf-8')
        k = quote_plus(str(k))
        if hasattr(v, '__iter__'):
            for x in v:
                if x.__class__ is unicode:
                    x = x.encode('utf-8')
                x = quote_plus(str(x))
                result += '%s%s=%s' % (prefix, k, x)
                prefix = '&'
        else:
            if v.__class__ is unicode:
                v = v.encode('utf-8')
            v = quote_plus(str(v))
            result += '%s%s=%s' % (prefix, k, v)
        prefix = '&'

    return result

def quote_plus(s, safe=''):
    """
    拷贝从 ``repoze.bfg`` <http://bfg.repoze.org>_
    
    Version of stdlib quote_plus which uses faster url_quote 
    """
    
    if ' ' in s:
        s = urlquote(s, safe + ' ')
        return s.replace(' ', '+')
    return urlquote(s, safe)

def urlsearch(pattern, path_info):
    """
    Example::
        
        matched_dict = urlsearch("/{userid}/blog/1234.html", environ["PATH_INFO"])
    
    .. note::
        
        pattern 不能包含端口
    """
    
    if not pattern.startswith("/"):
        pattern = "/" + pattern
    pattern = "^" + pattern
    pattern = pattern.replace(".", "\.")
    pattern = pattern.replace("{", "(?P<")
    pattern = pattern.replace("}", ">\w+).*")
    pattern = re.compile(pattern, re.U)
    if not path_info.startswith("/"):
        path_info = "/" + path_info
    matched = pattern.match(path_info)
    if matched is None:
        return {}
    return matched.groupdict()

def domainsearch(pattern, host):
    """
    Example::
        
        matched_dict = domainsearch("{userid}.i.example.com", environ["HTTP_HOST"])
    
    .. note::
        
        pattern 不能包含端口
    """
    
    pattern = pattern.replace(".", "\.")
    pattern = pattern.replace("{", "(?P<")
    pattern = pattern.replace("}", ">[a-z0-9\-]{1,62})")
    pattern = re.compile(pattern, re.U)
    if ":" in host:
        host = host.split(":")[0]
    matched = pattern.match(host)
    if matched is None:
        return {}
    return matched.groupdict()
    
def urlencrypt(url, secret):
    """
    用 Vignere 算法去加密一个 url, 如果 url 中包含文件名，则文件名部分不会加密
    
    :param url: url， 例如 /abc, /h/x.txt
    :param secret: 安全码
    :rtype: string
    
    .. seealso:: 
        
        :class:`khan.security.util.Vignere`, :func:`urldecrypt`
    """
    
    have_slash = url.startswith("/")
    if have_slash:
        path = url[1 : ]
    else:
        path = url
    basename = os.path.basename(path)
    if basename == "":
        return url
    vignere = Vignere(secret)
    if "." in  basename:
        ext = basename[basename.rfind(".") : ]
        text = vignere.encode(path[0 : path.rfind(".")]) + ext
    else:
        text = vignere.encode(path)
    if have_slash:
        text = "/" + text
    return text

def urldecrypt(url, secret):
    """
    用 Vignere 算法去解密一个用 :func:`urlencrypt` 加密过的 url
    
    :param url: url， 例如 /abc, /h/x.txt
    :param secret: 安全码，该参数应该与调用 :func:`urlencrypt` 时的一致
    :rtype: string
    
    .. seealso:: 
        
        :class:`khan.security.util.Vignere`, :func:`urlencrypt`
    """
    
    have_slash = url.startswith("/")
    if have_slash:
        new_url = url[1 : ]
    else:
        new_url = url
    if new_url == "":
        return url
    vignere = Vignere(secret)
    basename = os.path.basename(new_url)
    text = ""
    if "." in  basename:
        ext = basename[basename.rfind(".") : ]
        url_path = new_url[0 : new_url.rfind(".")]
        text = vignere.decode(url_path)
        text += ext
    else:
        text = vignere.decode(new_url)
    if have_slash:
        text = "/" + text
    return text

def get_wild_domain(domain):
    domain = domain.strip().strip(".")
    domain = remove_port_from_domain(domain)
    dot_num = domain.count(".")
    if dot_num in [0, 1]:
        return "." + domain
    else:
        return domain[domain[0 : domain.rfind(".")].rfind(".") : ]

def remove_port_from_domain(domain):
    if ":" in domain:
        return domain[0 : domain.find(":")]
    return domain

def fmt_url(url):
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        if url != "/" and not url.startswith("/"):
            url = "/" + url
    if url != "/" and url.endswith("/"):
        url = url[0 : -1]
    return url

class URLDecryptor(object):
    """
    本中间件将用 :func:`urlencrypt` 加密过的 url 解密，并重写 environ["PATH_INFO"] 的值为解密后的 url. 
    
    本中间件会设置两个环境变量::
    
        environ["khan.urldecryptor.orig_path_info"] = "未经解码的原始 URL"
        environ["khan.urldecryptor.orig_status_code"] = "被封装的 APP 返回的 http 状态码"
    
    .. seealso::
        
        :func:`urlencrypt`, :func:`urldecrypt`
    """
    
    def __init__(self, app, secret, instead_app = None):
        """
        :param app: wsgi app
        :param secret: 解码的 KEY， 该 KEY 应该和用 :func:`urlencrypt` 加密 url 时的 key 一样.
        :param instead_app: 如果被封装的 APP 没有返回 200 的 HTTP 状态，将调用该 APP 并返回，
            因为被调用的 APP 如果返回 HTTP 错误（例如状态码大于 400)时，可能会显示真实的客户端请
            求的 decoded 了的 URL，默认是 :class:`khan.httpstatus.HTTPStatus` (the app http status code). 
        
        :type app: wsgi app
        :type secret: string
        :type instead_app: wsgi app
        """
        
        self.app = app
        self.secret = secret
        self.instead_app = instead_app or self.inside_instead_app
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def bad_request_app(self, environ, start_response):
        app = HTTPStatus(400, environ["PATH_INFO"])
        return app(environ, start_response)
    
    def inside_instead_app(self, environ, start_response):
        extra = ""
        extra += '\nPATH_INFO: %r' % environ["PATH_INFO"]
        extra += '\nHTTP_HOST: %r' % environ.get('HTTP_HOST')
        app = HTTPStatus(environ["khan.urldecryptor.orig_status_code"], detail = environ["PATH_INFO"], comment=extra)
        return app(environ, start_response)
    
    def __call__(self, environ, start_response):
        path_info = environ.get("PATH_INFO", "")
        real_url = ""
        try:
            real_url = urldecrypt(path_info, self.secret)
        except:
            self.logger.debug("can't decode url '%s'" % path_info, exc_info = True)
            return self.bad_request_app(environ, start_response)
        new_environ = environ.copy()
        new_environ["PATH_INFO"] = real_url
        environ["khan.urldecryptor.orig_path_info"] = path_info
        self.logger.debug("overwrite PATH_INFO with '%s'" % real_url)
        app_code = []
        def repl_start_response(status, headers, exc_info=None):
            code = int(status.split(None, 1)[0])
            app_code.append(code)
            if code != 200:
                return lambda x : None
            return start_response(status, headers, exc_info)
        resp = self.app(new_environ, repl_start_response)
        environ["khan.urldecryptor.orig_status_code"] = app_code[0]
        if app_code[0] != 200:
            return self.instead_app(environ, start_response)
        else:
            return resp
        
def make_urldecryptor_middleware(global_conf, secret, instead_app = None):
    """
    Paste EGG entry point::
        
        urldecryptor
        
    PasteDeploy example::
    
        [filter:URLDecryptor]
        use = egg:khan#urldecryptor
        secret = 123456
        # instead_app = InternalErrorAapp
        
        [app:main]
        use = egg:paste#urlmap
        / = app1
    """
    
    if instead_app:
        config_file = global_conf["__file__"]
        instead_app = loadapp("config:%s" % config_file, instead_app, global_conf)
    def middleware(app):
        return URLDecryptor(app, secret, instead_app)
    return middleware

class RuleDispatcher(DictMixin):
    """
    根据正则表达式规则来匹配 url 并转发给不同的 app 处理
    
    本类实现了 Dict 接口, 实例::
        
        dispatcher = RuleDispatcher()
        dispatcher["/(.*).jpg"] = app1
        dispatcher["/(.*).png"] = app2
    """
    
    def __init__(self, default = None):
        """
        :param app: wsgi app
        """
        
        self.rule_map = {}
        self.map = {}
        self.default = default or HTTPStatus(404)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def __setitem__(self, rule, app):
        self.rule_map[rule] = app
        self.map[re.compile(rule)] = app
        
    def __delitem__(self, rule):
        del self.rule_map[rule]
        del self.map[re.compile(rule)] 
        
    def __getitem__(self, rule):
        return self.rule_map[rule]
    
    def keys(self):
        return self.rule_map.keys()
        
    def __call__(self, environ, start_response):
        path_info = environ.get("PATH_INFO", "")
        if path_info:
            for pattern, app in self.map.items():
                if pattern.match(path_info):
                    self.logger.debug("rule '%s' matched url '%s', dispatching to app '%s'" \
                                      % (pattern.pattern, path_info, get_request_handler_name(app)))
                    return app(environ, start_response)
        self.logger.debug("no rule matched url '%s'" % path_info)
        return self.default(environ, start_response)

def make_ruledispatcher_app(loader, global_conf, default = None, **rules):
    """
    Paste EGG entry point::
        
        ruledispatcher
        
    PasteDeploy example::
        
        [composite:RuleDispatcher]
        use = egg:khan#ruledispatcher
        /(.*)\.jpg = testapp
        /abc/(.*)\.html = testapp1
        
        [app:testapp]
        use = egg:paste#test
    """
    
    if default:
        default = loader.get_app(default)
    dispatcher = RuleDispatcher(default)
    for rule, app_name in rules.items():
        app = loader.get_app(app_name)
        if not app:
            raise ValueError("app '%s' not be found" % app_name)
        dispatcher[rule] = app
    return dispatcher

class FilterDispatcher(DictMixin, object):
    """
    根据正则表达式规则来匹配 url 并转发 app 给不同的中间件处理
    
    本类实现了 Dict 接口, 实例::
        
        dispatcher = FilterDispatcher(some_app)
        dispatcher["/(.*).jpg"] = imaging_middleware
        dispatcher["/(.*).png"] = imaging2_middleware
    """
    
    def __init__(self, app):
        """
        :param app: wsgi app
        """
        
        self.rule_map = {}
        self.map = {}
        self.app = app
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def __setitem__(self, rule, filter_factory):
        self.rule_map[rule] = filter_factory
        self.map[re.compile(rule)] = filter_factory(self.app)
        
    def __delitem__(self, rule):
        del self.rule_map[rule]
        del self.map[re.compile(rule)] 
        
    def __getitem__(self, rule):
        return self.rule_map[rule]
    
    def keys(self):
        return self.rule_map.keys()
        
    def __call__(self, environ, start_response):
        buf = []
        orig_response = []
        def repl_start_response(status, headers, exc_info=None):
            orig_response[ : ] = status, headers
            return lambda s : buf.append(s)
        path_info = environ.get("PATH_INFO", "")
        if path_info:
            for pattern, filter in self.map.items():
                if pattern.match(path_info):
                    self.logger.debug("rule '%s' matched url '%s', dispatching to filter '%s'" \
                                      % (pattern.pattern, path_info, get_request_handler_name(filter)))
                    app_iter = filter(environ, repl_start_response)
                    if not orig_response:
                        return HTTPStatus(500)(environ, start_response)
                    start_response(orig_response[0], orig_response[1])
                    return app_iter or buf
        app_iter = self.app(environ, repl_start_response)
        if not orig_response:
            return HTTPStatus(500)(environ, start_response)
        start_response(orig_response[0], orig_response[1])
        return app_iter or buf

def make_filterdispatcher_middleware(global_conf, conf = None, **rules):
    """
    Paste EGG entry point::
        
        ruledispatcher
        
    PasteDeploy example::
    
        [filter:URLDecryptor]
        use = egg:khan#urldecrypt
        key = 123456
        
        [filter-app:FilterDispatcher]
        use = egg:khan#filterdispatcher
        /(.*)\.jpg = URLDecryptor
        /abc/(.*)\.html = other_filter
        next = TestApp
        
        [app:TestApp]
        use = egg:paste#test
    """
    
    conf_file = conf or global_conf["__file__"]
    def middleware(app):
        dispatcher = FilterDispatcher(app)
        for rule, filter_uri in rules.items():
            filter_factory = loadfilter("config:" + conf_file, filter_uri, global_conf)
            dispatcher[rule] = filter_factory
        return dispatcher
    return middleware
