# -*- coding: utf-8 -*-

"""
访问限制 / 控制

索引
=================================

* :class:`RequestFrequencyRestrictor`
* :func:`make_request_frequency_restrictor_middleware`
* :class:`URLRestrictor`
* :func:`make_urlrestrictor_middleware`

=================================

.. autoclass:: RequestFrequencyRestrictor
.. autofunction:: make_request_frequency_restrictor_middleware
.. autoclass:: FilterRules
.. autoclass:: URLRestrictor
.. autofunction:: make_urlrestrictor_middleware
"""

import logging, time, re
from datetime import datetime, timedelta
from webob.exc import status_map
from enum import Enum
from UserList import UserList
from khan.deploy import loadapp
from khan.store import get_backend, ExpireStore
from khan.deploy import loadobject
from khan.httpstatus import HTTPStatus

__all__ = ["RequestFrequencyRestrictor", "URLRestrictor"]

class RequestFrequencyRestrictor(object):
    """
    本类允许设定客户端 (IP) 在间隔时间内对一个 WSGI APP 的请求次数进行限制
    """
    
    STORE_MAX_ENTRIES = 100000
    
    def __init__(self, app, frequency, interval, store = None, max_entries = STORE_MAX_ENTRIES, exc_app = None):
        """
        :param app: WSGI app
        :param frequency: 间隔时间内的最大允许请求频率(次数)
        :param interval: 间隔时间 (秒)
        :param store: 一个字典类型的存储介质, 用于存储用户的请求历史数据. 默认是内存存储
        :param max_entries: store 内的最大项目数, 此参数用于防止 store 过大
        :param exc_app: 当用户间隔时间内的请求频率超出限制，则调用该 app 返回给客户端, 默认是 403 
        """
        
        self.frequency = frequency
        self.interval = interval
        if store is None:
            store = get_backend("memory://")
        store = ExpireStore(store, max_entries = max_entries, expires = interval + (interval / 2))
        self._store = store
        self._exc_app = exc_app or status_map[403]()
        self.app = app
        self._logger = logging.getLogger(self.__class__.__name__)
        
    def __call__(self, environ, start_response):
        remote_addr = environ.get("REMOTE_ADDR", "")
        if remote_addr:
            self._logger.debug("can't get remote ip address")
            return self.app(environ, start_response)
        cur_time = int(time.time())
        if remote_addr not in self._store:
            self._store[remote_addr] = [cur_time]
            return self.app(environ, start_response)
        access_data = self._store[remote_addr]
        cur_datetime = datetime.fromtimestamp(cur_time)
        start_datetime = cur_datetime - timedelta(seconds = self.interval) 
        start_timestamp = int(time.mktime(start_datetime.timetuple()))
        access_data = filter(lambda x : x >= start_timestamp, access_data)
        if len(access_data) >= self.frequency:
            self._logger.debug("'%s' exceeded the frequency limit(%s)." % (remote_addr, self.frequency))
            return self._exc_app(environ, start_response)
        else:
            access_data.append(cur_time)
            self._store[remote_addr] = access_data
            return self.app(environ, start_response)

def make_request_frequency_restrictor_middleware(global_conf, frequency, interval, store = None, 
                                                 max_entries = None, exc_app = None, conf = None):
    """
    paste EGG Entry Point::
        
        request_frequency_restrictor
        
    用 PasteDeploy 部署::
    
        [filter-app:request_frequency]
        use = egg:khan#request_frequency_restrictor
        # 限制 60 秒之内访问 file app 最多 10 次
        frequency = 10
        interval = 60
        
        [app:file]
        use = egg:khan#file
        file = /etc/passwd
    """
    
    conf = conf or global_conf["__file__"]
    if exc_app:
        exc_app = loadapp("config:%s" % conf, exc_app, global_conf)
    frequency = int(frequency)
    interval = int(interval)
    if store:
        if "://" in store:
            store = get_backend(store)
        else:
            store = loadobject("config:%s" % conf, store, global_conf)
    if max_entries:
        max_entries = int(max_entries)
    else:
        max_entries = RequestFrequencyRestrictor.STORE_MAX_ENTRIES
    def middleware(app):
        app = RequestFrequencyRestrictor(app, frequency, interval, store, max_entries, exc_app)
        return app
    return middleware

class FilterRules(UserList):
    """
    URL 过滤规则容器，实现 List 接口，被 :class:`URLRestrictor` 用于存放过滤规则
    """
    
    def __init__(self, *args, **kargs):
        super(FilterRules, self).__init__(*args, **kargs)
        self.data = map(lambda x : re.compile(x), self.data)
        
    def append(self, rule):
        try:
            rule = re.compile(rule)
        except:
            raise ValueError("rule '%s' invalid." % rule)
        super(FilterRules, self).append(rule)
        
class URLRestrictor(object):
    """
    基于正则表达式的 URL 过滤.
    
    本类拥有一个黑名单规则和一个白名单规则, 当一个 url 试图通过检查时，
    本类首先会检查该 url 是否在白名单内，如果是则直接通过，否则再去检查该 url 是否在黑名单内，如果
    是则直接调用并返回 ``deny_handler`` 指定的 app 或者 ``on_deny`` 指定的 http 状态码, 如果该 url 不在
    白名单亦不在黑名单则直接通过检查.
    
    .. attribute:: blackrules 
        黑名单
    
    .. attribute:: whiterules 
        白名单
    """
    
    RuleAction = Enum("DENY", "ALLOW")
    
    def __init__(self, app, blackrules = None, whiterules = None, deny_handler = None):
        """
        :param app: wsgi app
        :param blackrules: 黑名单, 该参数同样可以通过 ``blackrules`` 属性设置
        :param whiterules: 白名单, 该参数同样可以通过 ``whiterules`` 属性设置
        :param deny_handler: 如果 url 不能通过检查则调用该 app 并返回
        
        :type app: wsgi app
        :type blackrules: :class:`FilterRules`
        :type whiterules: :class:`FilterRules`
        :type deny_handler: wsgi app
        """
        
        self.app = app
        if blackrules:
            if not isinstance(blackrules, FilterRules):
                blackrules = FilterRules(blackrules)
        else:
            blackrules = FilterRules()
        if whiterules:
            if not isinstance(whiterules, FilterRules):
                whiterules = FilterRules(whiterules)
        else:
            whiterules = FilterRules()
        self.blackrules = blackrules
        self.whiterules = whiterules
        self.deny_handler = deny_handler or HTTPStatus(403)
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def __call__(self, environ, start_response):
        path_info = environ.get("PATH_INFO", "")
        if self.whiterules:
            for white_rule in self.whiterules:
                if white_rule.match(path_info):
                    self.logger.debug("url '%s' in whiterules, passed." % path_info)
                    return self.app(environ, start_response)
        if self.blackrules:
            for black_rule in self.blackrules:
                if black_rule.match(path_info):
                    self.logger.debug("url '%s' in blackrules, blocked." % path_info)
                    return self.deny_handler(environ, start_response)
        return self.app(environ, start_response)
    
def make_urlrestrictor_middleware(global_conf, deny_handler = None, rulesets = None, 
                              conf = None, **rule_directives):
    """
    Paste EGG entry point::
        
        urlrestrictor
        
    PasteDeploy example::
    
        [filter:URLRestrictor]
        use = egg:khan#urlrestrictor
        #deny_handler = some_app
        rulesets = set1 set2
        rule /etc/(.*)\.(.*) = deny
        rule /etc/(.*)\.conf = allow
        
        [object:set1]
        use = egg:khan#dict
        /a/(.*)\.jpg = deny
        
        [object:set2]
        use = egg:khan#dict
        /b/(.*)\.jpg = allow
        
        [app:main]
        use = egg:paste#test
        filter-with = URLRestrictor
    """
    
    config_file = conf or global_conf["__file__"]
    if deny_handler:
        deny_handler = loadapp("config:" + config_file, deny_handler, global_conf)
    whiterules = FilterRules()
    blackrules = FilterRules()
    rules = {}
    for rule_directive, action in rule_directives.items():
        if rule_directive.startswith("rule "):
            rules[rule_directive[len("rule ") : ].strip()] = action
    if rulesets:
        for r in rulesets.split():
            rules.update(loadobject("config:%s" % config_file, r, global_conf))
    for rule, action in rules.items():
        if action == "allow":
            whiterules.append(rule)
        elif action == "deny":
            blackrules.append(rule)
        else:
            continue
    def middleware(app):
        return URLRestrictor(app, blackrules= blackrules, whiterules = whiterules, 
                             deny_handler = deny_handler)
    return middleware
