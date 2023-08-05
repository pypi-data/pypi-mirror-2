# -*- coding: utf-8 -*-

"""
事件通知与广播
=================================

索引
=================================

* :class:`Subscriber`
* :class:`AllEvent`
* :class:`AnySender`
* :class:`AnonymousSender`
* :class:`Notification`
* :class:`CallableSubscriber`
* :class:`CommandSubscriber`
* :class:`HTTPSubscriber`
* :class:`HTTPSender`
* :class:`HTTPBasedEventAgent`

* :func:`notify`
* :func:`try_notify`
* :func:`subscribe`
* :func:`unsubscribe`
* :func:`subscribed`
* :func:`make_httpsender_object`
* :func:`make_callable_subscriber_object`
* :func:`make_command_subscriber_object`
* :func:`make_http_subscriber_object`
* :func:`make_httpbasedeventagent_app`
* :func:`make_subscribed_object`

=================================

.. autoclass:: Subscriber
.. autoclass:: AllEvent
.. autoclass:: AnySender
.. autoclass:: AnonymousSender
.. autoclass:: Notification
.. autoclass:: CallableSubscriber
.. autoclass:: CommandSubscriber
.. autoclass:: HTTPSubscriber
.. autoclass:: HTTPSender
.. autoclass:: HTTPBasedEventAgent

.. autofunction:: notify
.. autofunction:: try_notify
.. autofunction:: subscribe
.. autofunction:: unsubscribe
.. autofunction:: subscribed
.. autofunction:: make_httpsender_object
.. autofunction:: make_callable_subscriber_object
.. autofunction:: make_command_subscriber_object
.. autofunction:: make_http_subscriber_object
.. autofunction:: make_httpbasedeventagent_app
.. autofunction:: make_subscribed_object
"""

import logging
from subprocess import Popen
from socket import gethostbyname
from paste.util.import_string import eval_import
from khan.utils import isiterable, Singleton
from khan.deploy import loadobject
from khan.json import JSONRPCService, JSONRPCClient, request as jrpc_req

__all__ = [
   "notify", 
   "try_notify", 
   "subscribe", 
   "unsubscribe", 
   "subscribed", 
   "CallableSubscriber",
   "CommandSubscriber",
   "HTTPSubscriber",
   "AllEvent",
   "AnySender",
   "AnonymousSender",
   "HTTPSender",
   "Notification",
   "HTTPBasedEventAgent"
]

class Subscriber(object):
    """
    所有 Subscriber 的基类
    """
    
    def notify(self, ntf):
        """
        :param ntf: :class:`Notification`
        """
        
        raise NotImplementedError

class AllEvent(object):
    """
    Used to represent 'all events'.
    """
    
    def __str__(self):
        return '<Event: %s>' % (self.__name__, )
    
class SenderMeta(type):
    
    """Base metaclass for sender classes."""

    def __str__(self):
        return '<Sender: %s>' % (self.__name__, )

class AnySender(object):
    """
    Used to represent either 'any sender'.

    The Any class can be used with connect, disconnect, send, or
    sendExact to denote that the sender paramater should react to any
    sender, not just a particular sender.
    """
    
    __metaclass__ = SenderMeta

class AnonymousSender(object):
    """
    Singleton used to signal 'anonymous sender'.

    The Anonymous class is used to signal that the sender of a message
    is not specified (as distinct from being 'any sender').
    Registering callbacks for Anonymous will only receive messages
    sent without senders.  Sending with anonymous will only send
    messages to those receivers registered for Any or Anonymous.

    Note: The default sender for connect is Any, while the default
    sender for send is Anonymous.  This has the effect that if you do
    not specify any senders in either function then all messages are
    routed as though there was a single sender (Anonymous) being used
    everywhere.
    """
    
    __metaclass__ = SenderMeta

class Notification(object):
    """
    事件通知
    
    .. attribute:: event
        
        事件
    
    .. attribute:: sender
    
        事件发送者
    
    .. attribute:: data
    
        事件数据
    """
    
    def __init__(self, event, sender = AnonymousSender, data = None):
        self.event = event
        self.data = data
        self.sender = sender
    
    def __repr__(self):
        return "<Notification (event = %r, sender = %r, data = %r)>" % (self.event, self.sender, self.data)
    
class CallableSubscriber(Subscriber):
    """
    封装一个可调用的 Python object 为一个 Subscriber
    """
    
    def __init__(self, callable):
        """
        :param callable: callable object
        """
        
        self.callable = callable
        
    def notify(self, ntf):
        return self.callable(ntf)

class CommandSubscriber(Subscriber):
    """
    封装一个命令行为 Subscriber, 命令行将运行于 sub-shell，命令行运行后不等待执行完成立即返回
    
    命令行内可使用以下三个替换变量:
    
        * $EVENT - 事件
        * $DATA - 事件数据
        * $SENDER -事件发送者
    """
    
    def __init__(self, cmdline):
        """
        :param cmdline: 命令行字符串
        """
        
        self.cmdline = cmdline
    
    def notify(self, ntf):
        cmdline = self.cmdline
        cmdline = cmdline.replace("$EVENT", "%r" % ntf.event)
        cmdline = cmdline.replace("$DATA", "%r" % ntf.data)
        cmdline = cmdline.replace("$SENDER", "%r" % ntf.sender)
        Popen(cmdline, shell = True)
        
class HTTPSubscriber(Subscriber):
    """
    通过 http 发送事件的发送器
    
    本类通过 jsonrpc 调用远程服务器公开的 jsonrpc service 的 notify(event, data) 方法来发送一个事件, 任何实现了 
    notify(event, data) 方法的 jsonrpc 服务都可以和本类配合使用, 例如 :class:`HTTPBasedEventAgent`.
    
    .. seealso::
        
        :class:`HTTPBasedEventAgent`, :class:`HTTPSender`
    """
    
    def __init__(self, url, timeout = 10):
        """
        url 规格::
        
            http://[username:password@]<host>[:port][/url]
        
        发送 url 示例::
            
            http://domain.com/
            
        带身份验证的发送 url 实例::
            
            http://username:password@www.example.com:999/notification
    
        :param url: url
        :param timeout: socket 级的 timeout 设置
        """
        
        self.timeout = timeout
        self.dest = url
        self._logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
    def notify(self, ntf):
        scheme, url = self.dest.split("://")
        username = None
        password = ""
        if "@" in url:
            credentials_part, service_url = url.split("@")
            if ":" in credentials_part:
                username, password = credentials_part.split(":")
            else:
                username = credentials_part
                password = ""
        else:
            service_url = url
        service_url = scheme + "://" + service_url
        client = JSONRPCClient(service_url, timeout = self.timeout)
        if username:
            client.add_credentials(username, password)
        self._logger.debug("send event to %s" % service_url)
        client.notify(ntf.event, ntf.data)

class HTTPSender(object):
    """
    通过 HTTP 发送的事件发送者
    
    .. seealso::
        
        :class:`HTTPSubscriber`, :class:`HTTPBasedEventAgent`
    """
    
    __metaclass__ = SenderMeta
    
    def __init__(self, host):
        """
        :param host: 主机地址，可为 IP 或者域名，例如: 127.0.0.1 或 domain.com
        :raise: host 无效
        """
        
        host = gethostbyname(host)
        self.host = host
    
    def __repr__(self):
        return "<HTTPSender (%r)>" % self.host
    
    def __cmp__(self, other):
        """
        如果两个 :class:`HTTPSender` 实例的 host 属性相等，则认为这两个对象是相等的
        """
        
        if isinstance(other, HTTPSender):
            return cmp(other.host, self.host)
        else:
            return -1

class HTTPBasedEventAgent(JSONRPCService):
    """
    一个 :class:`khan.json.JSONRPCService`, 公开一个名为 `notify` (event, data) 的 rpc 方法
    
    专门用于接收 :class:`HTTPSubscriber` 发送过来的事件，
    并调用本地的 notify(event, data, sender)， 其中 `sender` 为一个 :class:`HTTPSender` 对象
    
    订阅用法实例::
        
        @subscribed("UserCreated", HTTPSender("10.0.0.1"))
        def on_user_created(ntf):
            print ntf
            
    .. seealso::
        
        :class:`HTTPSubscriber`, :class:`HTTPSender`
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(HTTPBasedEventAgent, self).__init__()
        self["notify"] = self._notify
    
    def _notify(self, event, data):
        self.logger.debug("got event '%s' from %s. re-sent it." % (event, jrpc_req.remote_addr))
        notify(event, data, HTTPSender(jrpc_req.remote_addr))
        
class SubscriberFactory(Singleton):
    
    def __init__(self):
        self.subscribers = []
        
    def subscrube(self, subscriber, event, sender):
        item = (subscriber, event, sender)
        if item not in self.subscribers: 
            self.subscribers.append(item)
    
    def unsubscrube(self, subscriber, event, sender):
        item = (subscriber, event, sender)
        if item in self.subscribers:
            self.subscribers.remove((subscriber, event, sender))
    
    def __iter__(self):
        return iter(self.subscribers)
           
def notify(event, data = None, sender = AnonymousSender):
    """
    发送事件通知
    
    :param event: 事件，可为任意的 python object
    :param data: 事件数据，可为任意的 python object，建议只使用 Python 内置数据类型
    :param sender: 事件发送者，任意 python object.
    
    Example::
        
        notify("UserManager.Created", {"user" : "admin"})
        
    .. seealso::
        
        :func:`try_notify`
    """
    
    factory = SubscriberFactory()
    for subscriber, ev, sd in factory:
        if ev == event or ev == AllEvent:
            if sd == sender:
                try:
                    subscriber.notify(Notification(event, sender, data))
                except:
                    pass
            elif sd == AnySender:
                try:
                    subscriber.notify(Notification(event, sender, data))
                except:
                    pass
            elif ((sender == AnonymousSender) or (sender == None)) and ((sd == AnonymousSender) or (sd == None)):
                try:
                    subscriber.notify(Notification(event, sender, data))
                except:
                    pass

def try_notify(event, data = None, sender = AnonymousSender):
    """
    发送事件通知, 与 :func:`notify` 不同的是，如果任一 subscriber 抛出异常，则停止继续发送事件通知，并抛出该异常.
    
    :param event: 事件，可为任意的 python object
    :param data: 事件数据，可为任意的 python object，建议只使用 Python 内置数据类型
    :param sender: 事件发送者，任意 python object.
    
    .. seealso::
        
        :func:`notify`
    """
    
    factory = SubscriberFactory()
    for subscriber, ev, sd in factory:
        if ev == event or ev == AllEvent:
            if sd == sender:
                subscriber.notify(Notification(event, sender, data))
            elif sd == AnySender:
                subscriber.notify(Notification(event, sender, data))
            elif ((sender == AnonymousSender) or (sender == None)) and ((sd == AnonymousSender) or (sd == None)):
                subscriber.notify(Notification(event, sender, data))
                    
def subscribe(subscriber, event = AllEvent, senders = [AnySender]):
    """
    订阅一个事件
    
    :param subscriber: 订阅者对象
    :type subscriber: :class:`Subscriber`
    :param event: 匹配的事件，可为任意的 python object, 如果想订阅所有事件，则设置为 AllEvent
    :param senders: 
        要匹配事件发送者，可为任意的 python object.
        如设置为 :class:`AnySender` (默认) 则匹配任意的发送者，
        如设置为 :class:`AnonymousSender` 则仅匹配在调用 :func:`notify` 或 :func:`try_notify` 时 `sender` 参数 
        指定为 :class:`AnonymousSender` 或者 None 的情况.
    """
    
    if not isiterable(senders):
        senders = [senders]
    factory = SubscriberFactory()
    for sender in senders:
        factory.subscrube(subscriber, event, sender)


def unsubscribe(subscriber, event = AllEvent, senders = [AnySender]):
    """
    退订一个事件
    """
    
    if not isiterable(senders):
        senders = [senders]
    factory = SubscriberFactory()
    for sender in senders:
        factory.unsubscrube(subscriber, event, sender)

def subscribed(event = AllEvent, senders = [AnySender]):
    """
    订阅事件 decorator
    
    example1::
        
        @subscribed()
        def on_user_created(notification):
            pass
    
    example2::
        
        @subscribed("UserCreated")
        def on_user_created(notification):
            pass
    """
    
    def decorator(func):
        subscribe(CallableSubscriber(func), event, senders)
        return func
    return decorator
      
def make_httpsender_object(global_conf, host):
    """
    Paste EGG entry point::
        
        httpsender
        
    PasteDeploy example::
        
        [app:passport]
        use = egg:khan#passport
        event = subscribed
        
        [object:subscribed]
        use = egg:khan#subscribed
        UserCreated = callable_subsriber;httpsender
        
        [object:callable_subsriber]
        use = egg:khan#subscriber.callable
        callable = khan.test:subscriber
        
        [object:httpsender]
        use = egg:khan#httpsender
        host = 10.0.01
    """
    
    return HTTPSender(host)

def make_callable_subscriber_object(global_conf, callable):
    """
    Paste EGG entry point::
        
        subscriber.callable
        
    PasteDeploy example::
        
        [app:passport]
        use = egg:khan#passport
        event = subscribed
        
        [object:subscribed]
        use = egg:khan#subscribed
        UserCreated = callable_subsriber
        
        [object:callable_subsriber]
        use = egg:khan#subscriber.callable
        callable = khan.test:subscriber
    """
    
    return CallableSubscriber(eval_import(callable))
        
def make_command_subscriber_object(global_conf, command):
    """
    Paste EGG entry point::
        
        subscriber.command
        
    PasteDeploy example::
        
        [app:passport]
        use = egg:khan#passport
        event = subscribed
        
        [object:subscribed]
        use = egg:khan#subscribed
        UserCreated = command_subsriber
        
        [object:command_subsriber]
        use = egg:khan#subscriber.command
        command = /usr/bin/mycommand $EVENT
    """
    
    return CommandSubscriber(command)

def make_http_subscriber_object(global_conf, url, timeout = 10):
    """
    Paste EGG entry point::
        
        subscriber.http
        
    PasteDeploy example::
        
        [app:passport]
        use = egg:khan#passport
        event = subscribed
        
        [object:subscribed]
        use = egg:khan#subscribed
        UserCreated = http_subsriber
        
        [object:http_subsriber]
        use = egg:khan#subscriber.http
        url = http://www.example.com/httpbasedagent
        timeout = 30
    """
    
    timeout = int(timeout)
    return HTTPSubscriber(url, timeout = timeout)

def make_httpbasedeventagent_app(global_conf):
    """
    paste EGG Entry Point::
        
        eventagent
    
    用 PasteDeploy 部署::
    
        [app:eventagent]
        use = egg:khan#eventagent
    """
    
    return HTTPBasedEventAgent()

def make_subscribed_object(global_conf, conf = None, **map):
    """
    Paste EGG entry point::
        
        subscribed
        
    PasteDeploy example::
        
        [app:passport]
        use = egg:khan#passport
        event = subscribed
        
        [object:subscribed]
        use = egg:khan#subscribed
        UserCreated = callable_subsriber;ANY
        ALL =  callable_subsriber;ANONYMOUS
        
        [object:callable_subsriber]
        use = egg:khan#subscriber.callable
        callable = khan.test:subscriber
    """
    
    conf = conf or global_conf["__file__"]
    for event, subscriber_part in map:
        event = event.strip()
        if event.upper() in ["*", "ALL"]:
            ev = AllEvent
        else:
            ev = event
        if ";" in subscriber_part:
            subscriber, sender = subscriber_part.split(";")
            if sender.upper() == "ANY":
                sender = AnySender
            elif sender.upper() == "ANONYMOUS":
                sender = AnonymousSender
            else:
                sender = loadobject("config:%s" % conf, sender, global_conf)
        else:
            subscriber = subscriber_part
            sender = AnySender
        subscriber = loadobject("config:%s" % conf, subscriber, global_conf)
        subscribe(subscriber, ev, sender)
