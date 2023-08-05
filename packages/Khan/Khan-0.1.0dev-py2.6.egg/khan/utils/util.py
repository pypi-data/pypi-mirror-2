# coding: utf-8

"""
常用工具
=================================

索引
=================================

* :data:`requestTypes`
* :func:`request_classifier`
* :func:`abort`
* :func:`redirect_to`
* :func:`construct_path`
* :func:`get_mimetype`
* :func:`unique_id`
* :func:`classid`
* :func:`named_logger`
* :func:`isiterable`
* :func:`dispatch_on`
* :func:`aswsgi`
* :func:`ashandler`
* :class:`AsResponse`
* :class:`NoDefault`
* :class:`Singleton`

=================================

.. data:: requestTypes
    
    requestTypes = Enum("BROWSER", "DAV", "XMLPPC", "JSONRPC")
    
.. autofunction:: request_classifier
.. autofunction:: abort
.. autofunction:: redirect_to
.. autofunction:: construct_path
.. autofunction:: get_mimetype
.. autofunction:: unique_id
.. autofunction:: classid
.. autofunction:: named_logger
.. autofunction:: isiterable
.. autofunction:: dispatch_on
.. autofunction:: aswsgi
.. autofunction:: ashandler
.. autoclass:: AsResponse
.. autoclass:: NoDefault
.. autoclass:: Singleton
"""

import os, logging, mimetypes, urllib, \
    threading, hashlib, pkg_resources, time, random, uuid
from paste.httpheaders import REQUEST_METHOD, CONTENT_TYPE, USER_AGENT, WWW_AUTHENTICATE
from webob.exc import status_map
from webob import Request, Response
from enum import Enum
from khan import NAMESPACE
from .decorator import update_wrapper_for_handler

__all__ = [
   "requestTypes",
   "request_classifier",
   "abort", 
   "redirect_to",
   "construct_path",
   "get_mimetype",
   "unique_id",
   "classid",
   "named_logger",
   "isiterable",
   "get_request_handler_name",
   "AsResponse",
   "NoDefault",
   "dispatch_on", 
   "aswsgi", 
   "ashandler",
   "Singleton"
]

DAV_METHODS = (
    'OPTIONS',
    'PROPFIND',
    'PROPPATCH',
    'MKCOL',
    'LOCK',
    'UNLOCK',
    'TRACE',
    'DELETE',
    'COPY',
    'MOVE'
)

DAV_USERAGENTS = (
    'Microsoft Data Access Internet Publishing Provider',
    'WebDrive',
    'Zope External Editor',
    'WebDAVFS',
    'Goliath',
    'neon',
    'davlib',
    'wsAPI',
    'Microsoft-WebDAV'
    )

requestTypes = Enum("BROWSER", "DAV", "XMLPOST", "JSONPOST")

def request_classifier(environ):
    """ 
    Get request type

    如果传入对象不是字典类型，返回空字符串
    
    :param environ: wsgi environ dict
    
    :rtype: :data:`requestTypes` 或空字符串
    """

    # type is not dict, return empty str
    if not environ or len(environ) == 0:
        raise ValueError('environ is a empty or False or None object, please set it like dict or fill it data.')
    
    from khan.json import JSON_MIME_TYPE
    
    request_method = REQUEST_METHOD(environ)
    if request_method in DAV_METHODS:
        return requestTypes.DAV
    useragent = USER_AGENT(environ)
    if useragent:
        for agent in DAV_USERAGENTS:
            if useragent.find(agent) != -1:
                return requestTypes.DAV
    if request_method.lower() == "post":
        content_type = CONTENT_TYPE(environ)
        if content_type == "text/xml":
            return requestTypes.XMLPOST
        elif content_type in [JSON_MIME_TYPE, "text/javascript"]:
            return requestTypes.JSONPOST
    return requestTypes.BROWSER

UNKNOWN_MIMETYPE = "application/octet-stream"

def get_mimetype(filename, default = None):
    """
    取得一个文件的 mime 类型，如果类型未知则返回 `default` 参数
    
    :param filename: 文件名
    
    :rtype: string
    """
    
    return mimetypes.guess_type(filename)[0] or default

def named_logger(obj, dotted_path = None):
    if dotted_path:
        dotted_path + "."
    else:
        dotted_path = ""
    if isinstance(obj, basestring):
        name = obj
    else:
        name =  obj.__name__
    return logging.getLogger("%s%s" % (dotted_path, name))

def abort(status_code=None, detail="", headers=None, comment=None, **kargs):
    """
    终止当前请求并抛出一个 ``paste.httpexceptions.HTTPException``
    
    :param status_code: 状态码
    :param detail: 状态说明
    :param headers: 额外的 http 头， ``[(header_key, value)]`` 形式
    :param comment: 状态注释
    :exception paste.httpexceptions.HTTPException: ``paste.httpexceptions.HTTPException`` 子类
    
    .. note::
    
        要正常使用该函数必须加上 ``paste.httpexceptions.HTTPExceptionHandler``  中间件, 
        如果用 ``PasteDeploy`` 部署的话，只需加上 ``egg:paste#httpexceptions`` filter, 
        该中间件会将异常转换为 Response 返回,
    """
    
    logger = named_logger("abort", __name__)
    exc = status_map[status_code](detail=detail, headers=headers, comment=comment, **kargs)
    logger.debug("Aborting request, status: %s, detail: %r, headers: %r, "
              "comment: %r", status_code, detail, headers, comment)
    raise exc.exception

def redirect_to(location, status_code = 302):
    """
    Raises a ``paste.httpexceptions.HTTPFound``
    
    Optionally, a status_code variable ``may be`` passed with the status code of
    the redirect, ie::

        redirect_to('home_page', status_code=303)
    
    要正常使用该函数必须加上 egg:paste#httpexceptions 中间件
    """
    
    logger = named_logger("redirect_to", __name__)
    logger.debug("Raising redirect to %s", location)
    found = status_map[status_code]()
    found.location = location
    raise found.exception

def construct_path(environ):
    """
    取得当前请求的完整 path
    
    :param environ: wsgi environ
    
    :rtype: string
    """
    
    path = (environ.get("SCRIPT_NAME", "") + environ.get("PATH_INFO", ""))
    return urllib.quote(path)

def load_from_entry_point(entry_point, on_error = None):
    result = []
    for entrypoint in pkg_resources.iter_entry_points(entry_point):
        try:
            result.append((entrypoint, entrypoint.load()))
        except Exception, e:
            if callable(on_error):
                if on_error(e):
                    raise
            else:
                raise
    return result

def get_request_handler_name(handler):
    """
    取得一个 request handler 的字符串表示的名字，包括模块名

    传入对象失败(False)，返回空字符串
    
    (NOT TESTCASE)
    """

    # 对象失败，返回空字符串
    if not handler: 
        return ''
    
    # is function
    if hasattr(handler, "func_name"):
        return handler.__module__ + "." + handler.func_name
    # is class
    else:
        return handler.__module__ + "." + handler.__class__.__name__

def unique_id(url = None):
    """
    取得一个唯一的 id 标识
    
    :param url: 根据该 url 产生，如不提供则使用 :data:`khan.NAMESPACE`
    
    :rtype: string
    """
    
    r = [time.time(), random.random()]
    if hasattr(os, 'times'):
        r.append(os.times())
    md5_hash = hashlib.md5(str(r))
    try:
        unique_id = md5_hash.hexdigest()
    except AttributeError:
        # Older versions of Python didn't have hexdigest, so we'll
        # do it manually
        hexdigest = []
        for char in md5_hash.digest():
            hexdigest.append('%02x' % ord(char))
        unique_id = ''.join(hexdigest)
    result = (''.join(['%02d' % x for x in time.localtime(time.time())[:6]])
        + '-' + unique_id )
    return result

def classid(cls):
    name = cls.__module__ + "." + cls.__name__
    return str(uuid.uuid3(uuid.NAMESPACE_URL, NAMESPACE + "/" + "".join(map(lambda x : str(ord(x)), name))))

def isiterable(obj):
    return (not isinstance(obj, basestring)) and getattr(obj, '__iter__', False)
  
class NoDefault(object): pass

class SingletonMeta(type):
    '''
    Implement Pattern: SINGLETON
    (NO TESTCAST)
    '''

    __lockObj = threading.RLock()  # lock object
    __instance = None  # the unique instance

    def __call__(cls, *args, **kargs):
        '''Static method to have a reference to **THE UNIQUE** instance'''
        # Critical section start
        cls.__lockObj.acquire()
        try:
            if cls.__instance is None:
                #print cls, args, kargs
                # (Some exception may be thrown...)
                # Initialize **the unique** instance
                cls.__instance = type.__call__(cls, *args, **kargs)
                '''Initialize object **here**, as you would do in __init__()...'''
        finally:
            #  Exit from critical section whatever happens
            cls.__lockObj.release()
        # Critical section end
        return cls.__instance

class Singleton(object):
    
    __metaclass__ = SingletonMeta

class AsResponse(Response):
    """
    封装一个 wsgi app 为 ``webob.Response`` 对象

    (NO TESTCAST)
    
    example::
        
        def handler(req):
            return AsResponse(File("/etc/passwd"))
        
    ..note::
        
        所有 ``webob.Response`` 属性的读写访问均无效
    """
    
    def __init__(self, app):
        """
        :param app: wsgi app
        """
        
        self.app = app
        super(AsResponse, self).__init__()
    
    def __call__(self, environ, start_response):
        orig_response = []
        def repl_start_response(status, headers, exc_info=None):
            orig_response[ : ] = status, headers
            return lambda x : None
        app_iter = self.app(environ, repl_start_response)
        if orig_response:
            self.status = orig_response[0]
            self.headerlist.extend(orig_response[1])
        self.app_iter = app_iter
        return super(AsResponse, self).__call__(environ, start_response)

def dispatch_on(**method_map):
    """
    根据请求方法，转发请求到其他 webob handler 或者 wsgi app，如果匹配了请求方法则不再调用原本函数。
    
    例子::
        
        def show_form(environ, start_response):
            pass
        
        @dispatch_on(get = show_form)
        def save_form(environ, start_response):
            pass
    """
    
    # 将 key 全部转换为小写
    method_map = dict(map(lambda x : (x[0].lower(), x[1]), method_map.iteritems()))
    def d(handler):
        def dispatcher(*args, **kargs):
            """Wrapper for dispatch_on"""
            new_args = list(args)
            new_args.extend(kargs.values())
            # wsgi app
            if len(new_args) == 2:
                environ = new_args[0]
            # webob handler
            elif len(new_args) == 1:
                environ = new_args[0].environ
            else:
                raise ValueError("`handler` invalid")
    
            # 按照request方法，提取handler
            alt_handler = method_map.get(environ["REQUEST_METHOD"].lower())
            if alt_handler:
                logger = logging.getLogger(__name__ + ".dispatch_on()")
                logger.debug("Dispatching to %s instead", alt_handler)
                return alt_handler(*args, **kargs)
            return handler(*args, **kargs)
        return update_wrapper_for_handler(dispatcher, handler)
    return d

def aswsgi(app):
    """
    webob 函数转换为标准 wsgi app
    
    :param app: wsgi app
    :rtype: function
    
    示例::
        
        @aswsgi
        def app(req):
            return Response("body")
    
    .. seealso::
        
        :func:`ashandler`
    """
    
    def wrapper(environ, start_response):
        resp = app(Request(environ))
        return resp(environ, start_response)
    return update_wrapper_for_handler(wrapper, app)

def ashandler(app):
    """
    标准 wsgi app 转换为 webob 函数
    
    :param app: wsgi app
    :rtype: function
    
    示例::
        
        @ashandler
        def app(environ, start_response):
            start_response("200 OK", [("content-type", "plain/text")])
            return ["body"]

    .. seealso::
        
        :func:`aswsgi`
    """
    
    def wrapper(req):
        orig_response = []
        def repl_start_response(status, headers, exc_info=None):
            orig_response[ : ] = status, headers
            return lambda x : None
        app_iter = app(req.environ, repl_start_response)
        resp = Response(app_iter = app_iter)
        if orig_response:
            resp.status = orig_response[0]
            resp.headers = orig_response[1]
        return resp
    return update_wrapper_for_handler(wrapper, app)
