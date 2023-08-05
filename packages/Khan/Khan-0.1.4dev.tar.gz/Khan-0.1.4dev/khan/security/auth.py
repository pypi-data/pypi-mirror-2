# -*- coding: utf-8 -*-

"""
提供用户身份与权限验证功能
=================================

* :func:`authorize`
* :func:`make_authtkt_object`
* :func:`make_htpasswd_object`
* :func:`make_form_object`
* :func:`make_redirecting_form_object`
* :func:`make_basicauth_object`
* :func:`make_protector_middleware`
* :func:`make_auth_middleware`
* :func:`make_sessionidentifier_object`
* :func:`make_store_based_group_adapter`
* :func:`make_store_based_permission_adapter`
* :func:`make_storebasedauthenticator_object`
* :func:`make_storebasemetadataprovider_object`

* :class:`AuthTKT`
* :class:`SessionIdentifier`
* :class:`StoreBasedGroupAdapter`
* :class:`StoreBasedPermissionAdapter`
* :class:`StoreBasedAuthenticator`
* :class:`StoreBasedMetadataProvider`

=================================

.. autofunction:: authorize
.. autofunction:: make_authtkt_object
.. autofunction:: make_htpasswd_object
.. autofunction:: make_form_object
.. autofunction:: make_redirecting_form_object
.. autofunction:: make_basicauth_object
.. autofunction:: make_protector_middleware
.. autofunction:: make_auth_middleware
.. autofunction:: make_sessionidentifier_object
.. autofunction:: make_store_based_group_adapter
.. autofunction:: make_store_based_permission_adapter
.. autofunction:: make_storebasedauthenticator_object
.. autofunction:: make_storebasemetadataprovider_object

.. autoclass:: AuthTKT
.. autoclass:: SessionIdentifier
.. autoclass:: StoreBasedGroupAdapter
.. autoclass:: StoreBasedPermissionAdapter
.. autoclass:: StoreBasedAuthenticator
.. autoclass:: StoreBasedMetadataProvider
"""

import logging, os, datetime
from paste.util.import_string import eval_import
from repoze.what.middleware import setup_auth
from repoze.what.adapters import BaseSourceAdapter
from repoze.what import predicates
from repoze.what.predicates import not_anonymous, is_anonymous, Any, All
from repoze.who.interfaces import IAuthenticator, IChallenger, IIdentifier, IMetadataProvider
from repoze.who.plugins import htpasswd, form, basicauth, auth_tkt
from repoze.who.classifiers import default_challenge_decider
from webob.exc import status_map
from paste.util.converters import asbool
from zope.interface import implements
from khan.store import get_backend
from khan.utils import request_classifier, requestTypes
from khan.utils.decorator import update_wrapper_for_handler
from khan.utils.encryption import crypt
from khan.deploy import loadobject
from khan.session import session, SessionMiddleware
from khan.urlparse import get_wild_domain, remove_port_from_domain

__all__ = [
   "authorize", 
   "StoreBasedGroupAdapter", 
   "StoreBasedPermissionAdapter"
]

log = logging.getLogger(__name__)

def new_request_classifier(environ):
    req_type = request_classifier(environ)
    if req_type == requestTypes.BROWSER:
        return "browser"
    elif req_type == requestTypes.DAV:
        return "dav"
    elif req_type in [requestTypes.XMLPOST, requestTypes.JSONPOST]:
        return "rpc"
    return "browser"
        
def authorize(predicate):
    """
    decorator, 支持 webob handler 和 wsgi app, 用于身份验证和权限检查
    
    :param predicate: ``repoze.what.predicates.predicate``
    """
    
    def d(handler):
        def wrapper(*args, **kargs):
            new_args = list(args)
            new_args.extend(kargs.values())
            args_num = len(new_args)
            # handler is wsgi app
            if args_num == 2:
                environ = new_args[0]
            # `handler` is webob handler
            elif args_num == 1:
                environ = new_args[0].environ
            else:
                raise ValueError("`hanlder` invalid.")
            if not predicate.is_met(environ):
                if environ.get("repoze.who.identity", None):
                    log.error("403 Forbidden, access was denied to this resource '%s'." % environ.get("PATH_INFO", ""))
                    if args_num == 2:
                        return status_map[403]()(*args, **kargs)
                    else:
                        return status_map[403]()
                else:
                    log.error("401 Unauthorized on resource '%s'." % environ.get("PATH_INFO", ""))
                    if args_num == 2:
                        return status_map[401]()(*args, **kargs)
                    else:
                        return status_map[401]()
            return handler(*args, **kargs)
        return update_wrapper_for_handler(wrapper, handler)
    return d
        
def make_protector_middleware(global_conf, all = None, any = None, **options):
    """
    ``options``
        
        列出一个或者多个 predicate 配置选项,  例如::
            
            predicate = predicate args
             
    ``any``
        
        值可以为 ``options`` 内的一个或者多个 predicate 名, '*' 则代表 ``options`` 内出现的所有 predicate
    
    ``all``
        
        值可以为 ``options`` 内的一个或者多个 predicate 名, '*' 则代表 ``options`` 内出现的所有 predicate
        
    *当不指定 ``any`` 或者 ``all`` 选项时则默认为 ``all = *``*
        
    EGG Entry Point::
        
        protector
    
    用 PasteDeploy 部署::
    
        [filter:authorized]
        use = egg:khan#protector
        is_user = admin
        authenticated = True
        in_group = group_name
        in_all_groups = group1 group2
        in_any_group = group1 group2
        has_permission = read
        has_all_permissions = read write
        has_any_permission = read write
        # any/all 选项只能出现其一
        # any = is_user in_group
        all = is_user in_group
        
        [app:test]
        use = egg:paste#test
        filter-with = authorized
    """
    
    def middleware(app):
        if any:
            if any.strip() == "*":
                objects = options
            else:
                predicate_names = any.split()
                objects = filter(lambda key, value : key in predicate_names, options.items())
        elif all:
            if all.strip() == "*":
                objects = options
            else:
                predicate_names = all.split()
                objects = filter(lambda key, value : key in predicate_names, options.items())
        else:
            objects = options
        predicate_list = []
        for cls_name, args_str in objects.items():
            args_str = args_str.strip()
            if cls_name == "authenticated":
                if asbool(args_str):
                    predicate_list.append(not_anonymous())
                else:
                    predicate_list.append(is_anonymous())
                continue
            if hasattr(predicates, cls_name):
                predicate_cls = getattr(predicates, cls_name)
                args = args_str.split()
                try:
                    predicate_list.append(predicate_cls(*args))
                except TypeError:
                    raise ValueError("'%s' option value '%s' invalid." % (cls_name, args_str))
            else:
                raise ValueError("'%s' option invalid." % cls_name)
        # 如果用户不指定任何的 predicate，则默认用 not_anonymous()
        if not predicate_list:
            predicate_list.append(not_anonymous())
        if len(predicate_list) == 1:
            predicate =  predicate_list[0]
        else:
            if any:
                predicate = Any(*predicate_list)
            else:
                predicate = All(*predicate_list)
        return authorize(predicate)(app)
    return middleware
    
def parse_who_plugins(global_conf, config, plugin_names, iface):
    result = []
    if isinstance(plugin_names, basestring):
        plugin_names = plugin_names.split()
    for name in plugin_names:
        if ";" in name:
            plugin_name, classifier = name.split(";")
        else:
            plugin_name = name
            classifier = None

        plugin = loadobject("config:%s" % config, plugin_name, global_conf)
        if plugin is None:
            raise ValueError("plugin '%s' can't load failure." % name)
        if classifier is not None:
            classifications = getattr(plugin, "classifications", None)
            if classifications is None:
                classifications = plugin.classifications = {}
            classifications[iface] = classifier

        result.append((plugin_name, plugin))
    return result

def parse_what_plugins(global_conf, config, plugin_names):
    result = {}
    if isinstance(plugin_names, basestring):
        plugin_names = plugin_names.split()
    for name in plugin_names:
        plugin = loadobject("config:%s" % config, name, global_conf)
        if plugin is None:
            raise ValueError("plugin '%s' can't load failure." % name)
        result[name] = plugin
    return result
              
def make_auth_middleware(global_conf, identifiers, authenticators, challengers, mdproviders = None, 
     group_adapters = None, permission_adapters = None, conf = None, request_classifier = None,  
     challenge_decider = None,  skip_authentication = False):
    """
    EGG Entry Point::
        
        auth
    
    用 PasteDeploy 部署::
            
        [filter-app:auth]
        use = egg:khan#auth.auth
        next = site
        identifiers = form;browser auth_tkt basicauth
        authenticators = htpasswd
        challengers = form;browser basicauth
        # 可选，如果你想使用组验证的话
        group_adapters = group
        # 可选，如果你想使用 permission 验证的话
        permission_adapters = permission
        
        [object:form]
        use = egg:khan#auth.form
        login_form_qs = __do_login
        rememberer_name = auth_tkt
        template_render = package.module:template_render
        
        [object:auth_tkt]
        use = egg:khan#auth.auth_tkt
        
        [object:basicauth]
        use = egg:khan#auth.basicauth
        
        [object:htpasswd]
        use = egg:khan#auth.htpasswd
        filename = %(here)s/%(package)s/conf/account.conf
        
        [object:group]
        use = egg:khan#auth.store_based_group
        store = khan.ini://%(here)s/%(package)s/conf/group.conf
        
        [object:permission]
        use = egg:khan#auth.store_based_permission
        store = khan.ini://%(here)s/%(package)s/conf/permission.conf
    """
    
    config_file = conf or global_conf["__file__"]
    identifier_plugins = parse_who_plugins(global_conf, config_file, identifiers, IIdentifier)
    authenticator_plugins = parse_who_plugins(global_conf, config_file, authenticators, IAuthenticator)
    challenger_plugins = parse_who_plugins(global_conf, config_file, challengers, IChallenger)
    if mdproviders:
        mdprovider_plugins = parse_who_plugins(global_conf, config_file, mdproviders, IMetadataProvider)
    else:
        mdprovider_plugins = []
    if group_adapters:
        group_adapter_plugins = parse_what_plugins(global_conf, config_file, group_adapters)
    else:
        group_adapter_plugins = None
    if permission_adapters:
        permission_adapter_plugins = parse_what_plugins(global_conf, config_file, permission_adapters)
    else:
        permission_adapter_plugins = None
    def middleware(app):
        return setup_auth(app,
              group_adapters=group_adapter_plugins,
              permission_adapters=permission_adapter_plugins,
              identifiers=identifier_plugins,
              authenticators=authenticator_plugins,
              challengers=challenger_plugins,
              mdproviders=mdprovider_plugins,
              classifier=request_classifier and eval_import(request_classifier) or new_request_classifier,
              challenge_decider=challenge_decider and eval_import(challenge_decider) or default_challenge_decider,
              skip_authentication = asbool(skip_authentication),
              log_stream = log,
              log_level = asbool(global_conf.get("debug", False)) and logging.DEBUG or logging.INFO 
        )
    return middleware

class StoreBasedGroupAdapter(BaseSourceAdapter):
    """repoze.what 的 Group 数据存储的 dict 源适配器
    
    ``store`` 为一个 dict like 的对象，store 数据形式应该为以下两种之一：
    
    .. code-block:: python
        
        {"group1" : ["user1", "user2"], "group2" : ["user3", "user4"]}
        
    .. code-block:: python
        
        {"group1" : "user1 user2", "group2" : "user3 user4"}
    """

    def __init__(self, store, writable = True):
        """
        :param store: dict like object
        :param writable: dict writable?
        """
        
        super(StoreBasedGroupAdapter, self).__init__(writable = writable)
        data = {}
        for group_name, users in store.items():
            if isinstance(users, basestring):
                users = users.split()
            data[self._encoding(group_name)] = set(map(lambda item: self._encoding(item), users))
        self._store = data
        self.store = store
        
    def _encoding(self, value):
        if not isinstance(value, unicode):
            return value.decode("utf-8")
        return value
    
    def _get_all_sections(self):
        return self._store

    def _get_section_items(self, section):
        return self._store[section]

    def _find_sections(self, credentials):
        username = credentials["repoze.what.userid"]
        return set([n for (n, g) in self._store.items() if username in g])

    def _include_items(self, section, items):
        self._store[section] |= items
        self.store[section] = " ".join(self._store[section])
        
    def _exclude_items(self, section, items):
        for item in items:
            self._store[section].remove(item)
        self.store[section] = " ".join(self._store[section])
            
    def _item_is_included(self, section, item):
        return item in self._store[section]

    def _create_section(self, section):
        self._store[section] = set()
        self.store[section] = ""
        
    def _edit_section(self, section, new_section):
        orig_section = set()
        orig_section.update(self._store[section])
        self._store[new_section] = orig_section
        self.store[new_section] = " ".join(orig_section)
        del self._store[section]
        del self.store[section]

    def _delete_section(self, section):
        del self._store[section]
        del self.store[section]
        
    def _section_exists(self, section):
        return self._store.has_key(section)

def make_store_based_group_adapter(global_conf, store, section = None, writable = True, conf = None):
    """
    EGG Entry Point::
        
        auth.store_based_group
    
    用 PasteDeploy 部署::
    
        [filter-app:auth]
        use = egg:khan#auth
        next = site
        identifiers = form;browser session auth_tkt
        authenticators = htpasswd
        challengers = form;browser
        group_adapters = group
        permission_adapters = permission
    
        [object:group]
        use = egg:khan#auth.store_based_group
        writeable = True
        store = khan.ini://%(here)s/%(package)s/conf/group.conf
    
    .. seealso::
        
        :class:`StoreBasedGroupAdapter`, :func:`make_auth_middleware`
    """
    
    conf = conf or global_conf["__file__"]
    writable = asbool(writable)
    if "://" in store:
        store = get_backend(store)
    else:
        store = loadobject("config:%s" % conf, store, global_conf)
    if section:
        store = store[section]
    return StoreBasedGroupAdapter(store, writable = writable)
    
class StoreBasedPermissionAdapter(BaseSourceAdapter):
    """repoze.what 的 Permission 数据存储的 dict 源适配器
    
    ``store`` 为一个 dict like 的对象，store 数据形式应该为以下两种之一：
    
    .. code-block:: python
        
        {"create-user" : ["group1", "group2"], "remove-user" : ["group3", "group4"]}
    
    .. code-block:: python
        
        {"create-user" : "group1 group2", "remove-user" : "group3 group4"}
    """

    def __init__(self, store, writable = True):
        """
        :param store: dict like object
        :param writable: dict writable?
        """
        
        super(StoreBasedPermissionAdapter, self).__init__(writable = writable)
        data = {}
        for permission_name, groups in store.items():
            if isinstance(groups, basestring):
                groups = groups.split()
            data[self._encoding(permission_name)] = set(map(lambda item: self._encoding(item), groups))
        self._store = data
        self.store = store
        
    def _encoding(self, value):
        if not isinstance(value, unicode):
            return value.decode("utf-8")
        return value
    
    def _get_all_sections(self):
        return self._store

    def _get_section_items(self, section):
        return self._store[section]

    def _find_sections(self, group_name):
        return set([n for (n, p) in self._store.items() if group_name in p])

    def _include_items(self, section, items):
        self._store[section] |= items
        self.store[section] = " ".join(self._store[section])
        
    def _exclude_items(self, section, items):
        for item in items:
            self._store[section].remove(item)
        self.store[section] = " ".join(self._store[section])
            
    def _item_is_included(self, section, item):
        return item in self._store[section]

    def _create_section(self, section):
        self._store[section] = set()
        self.store[section] = ""
        
    def _edit_section(self, section, new_section):
        orig_section = set()
        orig_section.update(self._store[section])
        self._store[new_section] = orig_section
        self.store[new_section] = " ".join(orig_section)
        del self._store[section]
        del self.store[section]
        
    def _delete_section(self, section):
        del self._store[section]
        del self.store[section]
        
    def _section_exists(self, section):
        return self._store.has_key(section)

def make_store_based_permission_adapter(global_conf, store, section = None, writable = True, conf = None):
    """
    EGG Entry Point::
        
        auth.store_based_permission
    
    用 PasteDeploy 部署::
    
        [filter-app:auth]
        use = egg:khan#auth
        next = site
        identifiers = form;browser session auth_tkt
        authenticators = htpasswd
        challengers = form;browser
        group_adapters = group
        permission_adapters = permission
    
        [object:permission]
        use = egg:khan#auth.store_based_permission
        writable = True
        store = khan.ini://%(here)s/%(package)s/conf/permission.conf
    
    .. seealso::
        
        :class:`StoreBasedPermissionAdapter`, :func:`make_auth_middleware`
    """
    
    conf = conf or global_conf["__file__"]
    writable = asbool(writable)
    if "://" in store:
        store = get_backend(store)
    else:
        store = loadobject("config:%s" % conf, store, global_conf)
    if section:
        store = store[section]
    return StoreBasedPermissionAdapter(store, writable = writable)

_NOW_TESTING = None  # unit tests can replace
def _now():  #pragma NO COVERAGE
    if _NOW_TESTING is not None:
        return _NOW_TESTING
    return datetime.datetime.now()

class AuthTKT(auth_tkt.AuthTktCookiePlugin):
    """
    :class:`AuthTKT` 插件是一个实现了 IIdentifier 的 auth 插件, 本插件可从将用户信息写入客户端 cookie， 可实现
    “记住用户” 的功能，在 cookie 过期之前，用户不需再次登录.
    """
    
    implements(IIdentifier, IAuthenticator)

    TICKET_NAME = "X-Kh-Auth"
    
    def __init__(self, secret, cookie_name=TICKET_NAME,
                 secure=False, include_ip=False,
                 timeout=None, reissue_time=None, userid_checker=None):
        super(AuthTKT, self).__init__(secret, cookie_name, secure, include_ip, timeout, reissue_time, userid_checker)
    
    def _get_cookies(self, environ, value, max_age=None):
        """
        重写本方法确保 wild_domain 正确， who 目前的实现有问题
        """
        
        if max_age is not None:
            later = _now() + datetime.timedelta(seconds=int(max_age))
            # Wdy, DD-Mon-YY HH:MM:SS GMT
            expires = later.strftime('%a, %d %b %Y %H:%M:%S')
            # the Expires header is *required* at least for IE7 (IE7 does
            # not respect Max-Age)
            max_age = "; Max-Age=%s; Expires=%s" % (max_age, expires)
        else:
            max_age = ''
        cur_domain = remove_port_from_domain(environ.get("HTTP_HOST", environ.get("SERVER_NAME")))
        wild_domain = get_wild_domain(cur_domain)
        cookies = [
            ('Set-Cookie', '%s="%s"; Path=/%s' % (
            self.cookie_name, value, max_age)),
            ('Set-Cookie', '%s="%s"; Path=/; Domain=%s%s' % (
            self.cookie_name, value, cur_domain, max_age)),
            ('Set-Cookie', '%s="%s"; Path=/; Domain=%s%s' % (
            self.cookie_name, value, wild_domain, max_age))
            ]
        return cookies

def make_authtkt_object(global_conf, secret=None,
                secretfile=None,
                cookie_name=AuthTKT.TICKET_NAME,
                secure=False,
                include_ip=False,
                timeout=None,
                reissue_time=None,
                userid_checker=None,
               ):
    """
    :param global_conf: global config
    :param secret: 用于加密存放到客户端 cookie 信息的安全码，如不提供则用 :func:`khan.utils.unique_id` 生成一个
    :param secretfile: 用于加密存放到客户端 cookie 信息的安全码，如不提供则用 :func:`khan.utils.unique_id` 生成一个
    :param cookie_name: cookie name, 默认为 :data:`AuthTKT.TICKET_NAME`
    :param secure: 对应 cookie 的 secure 段 (参看cookie规范)
    :param include_ip: 是否将客户端 IP 同时记录在 cookie 中，如果下次用户再次访问的话，
        如果 IP 与之前cookie中保存的 IP 不一样，则视该 cookie 无效。
        
    .. seealso::
        
        :class:`AuthTKT` 
        
    EGG Entry Point::
        
        auth.auth_tkt
    
    用 PasteDeploy 部署::
    
        [object:auth_tkt]
        use = egg:khan#auth.auth_tkt
        # 可选, cookie name
        name = Auth
        # 用于加密 cookie 数据的安全码
        secret = ahjsdh
        # 可选，这里设置 cookie 到期时间为一年
        expires = 31536000
        # 可选
        include_ip = True
        # 可选
        secure = True
    
    .. seealso::
        
        :func:`make_auth_middleware`
    """
    
    if secretfile:
        secretfile = os.path.abspath(os.path.expanduser(secretfile))
        if not os.path.exists(secretfile):
            raise ValueError("No such 'secretfile': %s" % secretfile)
        secret = open(secretfile).read().strip()
    elif not secret:
        raise ValueError("One of the `secret` and `secretfile` must specified.")
    if timeout:
        timeout = int(timeout)
    if reissue_time:
        reissue_time = int(reissue_time)
    if userid_checker is not None:
        userid_checker = eval_import(userid_checker)
    plugin = AuthTKT(secret, cookie_name,
                                 asbool(secure),
                                 asbool(include_ip),
                                 timeout,
                                 reissue_time,
                                 userid_checker,
                                 )
    return plugin

def make_htpasswd_object(global_conf, filename, check_fn = None):
    """
    HTPasswd 插件是一个实现了 IAuthenticator 的 auth 插件, 本插件可从一个 Apache 风格的 htpasswd 配置文件中
    读取用户名和密码信息来校验.
    
    :param global_conf: global config
    :param filename: 包含用户名密码的文件
    :param check_fn: 密码校验函数, 签名必须为 ``check_fn(password, hashed)``, 
        ``password`` 参数为明文, ``hashed`` 为存储在 ``filename`` 文件中的密码
    
    EGG Entry Point::
        
        auth.htpasswd
    
    用 PasteDeploy 部署::
    
        [object:htpasswd]
        use = egg:khan#auth.htpasswd
        filename = %(here)s/%(package)s/conf/passwd
        # 可选，默认用 UNIX 中的 crypt()
        check_fn = package.module:check_fn
    """
    
    check_fn = check_fn or "repoze.who.plugins.htpasswd:crypt_check"
    return htpasswd.make_plugin(filename, check_fn)

def make_form_object(global_conf, *args, **kargs):
    """
    Form 插件是一个实现了 IIdentifier 和 IChallenger 的 auth 插件 
    
    :param global_conf: global config
    :param rememberer_name:  其他 auth 插件名，用于被 RedirectingForm 插件调用执行 remember 和 forget 操作
    :param login_form_qs: 当 GET 参数中含有该 key 才认为用户 POST 登录数据
    
    EGG Entry Point::
        
        auth.form
    
    用 PasteDeploy 部署::
    
        [object:form]
        use = egg:khan#auth.form
        login_form_qs = __do_login
        rememberer_name = session
    
    .. seealso::
        
        :func:`make_auth_middleware`
    """
    
    return form.make_plugin(*args, **kargs)

def make_redirecting_form_object(global_conf, *args, **kargs):
    """
    RedirectingForm 插件是一个实现了 IIdentifier 和 IChallenger 的 auth 插件 
    
    :param global_conf: global config
    :param rememberer_name:  其他 auth 插件名，用于被 RedirectingForm 插件调用执行 remember 和 forget 操作
        用于被 RedirectingForm 插件调用执行 remember 和 forget 操作
    :param login_form_url: 登录表单的 url, 表单的提交目标地址必须为 ``login_handler_path`` 参数指定的地址，且必须有名为
         login 和 password 的字段
    :param login_handler_path: 接收登录表单 POST 数据的 url path
    :param logout_handler_path: 登出 url
    
    EGG Entry Point::
        
        auth.redirecting_form
    
    用 PasteDeploy 部署::
    
        [object:form]
        use = egg:khan#auth.redirecting_form
        login_form_url = /account/login
        login_handler_path = /account/do_login
        logout_handler_path = /account/logout
        rememberer_name = session
    
    .. seealso::
        
        :func:`make_auth_middleware`
    """
    
    return form.make_redirecting_plugin(*args, **kargs)

def make_basicauth_object(global_conf, realm = None):
    """
    BasicAuth 插件是一个实现了 IIdentifier 和 IChallenger 的 auth 插件, 提供 HTTP basicauth 验证 
    
    EGG Entry Point::
        
        auth.basicauth
    
    用 PasteDeploy 部署::
    
        [object:basicauth]
        use = egg:khan#auth.basicauth
        # optional
        realm = "KhanSite Login"
        
    .. seealso::
        
        :func:`make_auth_middleware`
    """
    
    realm = realm or "Login"
    return basicauth.make_plugin(realm = realm)

def default_password_compare(cleartext_password, stored_password_hash):
    return crypt(cleartext_password) == stored_password_hash

class SessionIdentifier(object):
    """
    SessionIdentifier 插件是一个实现了 IIdentifier auth 插件, 允许将用户标识数据存储在 session 中
    
    .. note::
        
        必须启用 :class:`khan.session.SessionMiddleware` 中间件
    """
    
    implements(IIdentifier)
    
    DEFAULT_KEY = "__IDENTITY"
    
    def __init__(self, key=DEFAULT_KEY):
        self.key = key
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def identify(self, environ):
        if SessionMiddleware.ENVIRON_KEY in environ:
            if self.key in session:
                return session[self.key]
        else:
            self._logger.error("`SessionMiddleware` no setup.")
    
    def remember(self, environ, identity):
        if SessionMiddleware.ENVIRON_KEY in environ:
            
            # FIXME: 更加好的方法排除 identity 内不必须的对象
            # FIXME: 只需要 login max_age 两个关键字，其他似乎没有必要用到
            session[self.key] = identity
            session.save()
            self._logger.info("remember identity to %s's session." % (identity.get('login')))
        else:
            self._logger.error("`SessionMiddleware` no setup.")
    
    def forget(self, environ, identity):
        if SessionMiddleware.ENVIRON_KEY in environ:
            if self.key in session:
                del session[self.key]
                session.save()
                self._logger.debug("forget identity from %s's session." % (identity.get("login")))
        else:
            self._logger.error("`SessionMiddleware` no setup.")

def make_sessionidentifier_object(global_conf, **kw):
    """
    EGG Entry Point::
        
        auth.session
    
    用 PasteDeploy 部署::
    
        [object:session]
        use = egg:khan#auth.session
        
    .. seealso::
        
        :class:`Session`, :func:`make_auth_middleware`, :mod:`khan.session`
    """
    
    return SessionIdentifier(**kw)


class StoreBasedAuthenticator(object):
    """
    store 必须为以下形式:
    
    store["user"] = {"password" : "pwd", "meta" : "xxx"}
    """
    
    implements(IAuthenticator)
    
    def __init__(self, store, compare_fn = None):
        self.compare_fn = compare_fn or default_password_compare
        self.store = store

    def authenticate(self, environ, identity):
        if not 'login' in identity:
            return None
        user_id = identity["login"]
        if user_id not in self.store:
            return None
        meta = self.store[user_id]
        if "password" not in meta:
            return None
        password = meta["password"]
        if not isinstance(password, basestring):
            password = "%s" % password
        if self.compare_fn(identity['password'], password):
            return user_id

def make_storebasedauthenticator_object(global_conf, store, compare_fn = None):
    if "://" in store:
        store = get_backend(store)
    else:
        store = loadobject("config:%s" % global_conf["__file__"], store, global_conf)
    if compare_fn:
        compare_fn = eval_import(compare_fn)
    return StoreBasedAuthenticator(store, compare_fn = compare_fn)

class StoreBasedMetadataProvider(object):
    
    implements(IMetadataProvider)
    
    def __init__(self, store, name = "user"):
        self.name = name
        self.store = store
        
    def add_metadata(self, environ, identity):
        userid = identity['repoze.who.userid']
        if userid in self.store:
            md = dict(self.store[userid])
            if md:
                if self.name in identity:
                    if hasattr(identity[self.name], "update"):
                        environ['repoze.who.logger'].debug("Update the metadata **%r to identify[%r]" 
                                                           % (md, self.name))
                        identity[self.name].update(md)
                    else:
                        environ['repoze.who.logger'].debug("Can't update the metadata **%r to identify, key '%s' exists" 
                                                           % (md, self.name))
                        return
                else:
                    identity[self.name] = md

def make_storebasemetadataprovider_object(global_conf, store, name = "user"):
    if "://" in store:
        store = get_backend(store)
    else:
        store = loadobject("config:%s" % global_conf["__file__"], store, global_conf)
    return StoreBasedMetadataProvider(store, name)
