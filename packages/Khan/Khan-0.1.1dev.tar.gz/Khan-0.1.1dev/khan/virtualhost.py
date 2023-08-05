# -*- coding: utf-8 -*-

"""
虚拟主机支持
=================================

索引
=================================

* :class:`VirtualHost`
* :func:`make_virtualhost_app`

=================================

.. autoclass:: VirtualHost
.. autofunction:: make_virtualhost_app
"""

import logging, re
from UserDict import UserDict
from khan.httpstatus import HTTPStatus

__all__ = ["VirtualHost"]

class VirtualHost(UserDict):
    """
    根据主机名和端口规则来转发请求给不同的 app.
    
    规则为 ``domain:port`` 形式的字符串, ``*`` 为通配符，可匹配任意 domain 部分和 port
    
    本类实现 dict 接口，转发规则即为 key, 规则对应的 app 即为 value, 实例::
        
        vhost = VirtualHost()
        vhost["domain1.com"] = app1
        vhost["domain2.com:8080"] = app2
        vhost["*.domain3.com"] = app3
        vhost["*:*"] = app4
        vhost["*:90] = app5
    """
    
    def __init__(self, default = None):
        """
        :param default: 默认 app, 当没有匹配任何 app 的时候, 该默认 app 将被用来处理请求，
            默认 app 会直接返回 404
        """
        
        self.default = default or HTTPStatus(404)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data = {}
        self.sorted_route_table = []
        
    def __setitem__(self, spec, app):
        spec = spec.strip()
        if ":" in spec:
            domain, port = spec.split(":")
            domain = domain.strip()
            port = port.strip()
            if port:
                if port == "*":
                    port = None
                else:
                    port = int(port)
            else:
                port = None
        else:
            domain = spec.strip()
            port = None
        if (not domain) or domain == "*":
            domain = None
            domain_pat = None
        else:
            domain = domain.lower()
            domain_pat = None
            try:
                domain_pat = "^" + domain.replace(".", "\.").replace("*", "(.*)") + "$"
                domain_pat = re.compile(domain_pat)
            except:
                raise KeyError("domain spec '%s' invalid." % domain)
        UserDict.__setitem__(self, spec, (domain_pat, domain, port, app))
        self.resort()
        
    def __getitem__(self, spec):
        app = UserDict.__getitem__(self, spec)[3]
        return app
    
    def __delitem__(self, spec):
        UserDict.__delitem__(self, spec)
        self.resort()
        
    def resort(self):
        def sort(x, y):
            domain_pat, domain, port, app = x[1]
            domain_pat1, domain1, port1, app1 = y[1]
            if domain1 and ("*" not in domain1) and domain and ("*" in domain):
                pat = re.compile(domain.replace(".", "\."))
                if pat.match(domain1):
                    return -1
                return 0
            elif domain and ("*" not in domain) and domain1 and ("*" in domain1):
                return 1
            return cmp(domain, domain1) or cmp(port, port1)
        def reverse_string_from_item(item):
            domain_pat, domain, port, app = item[1]
            if not domain_pat:
                return item
            x = list(domain)
            x.reverse()
            x = "".join(x)
            return (item[0], (domain_pat, x, port, app))
        data = map(reverse_string_from_item, self.data.items())
        data.sort(sort)
        data = map(reverse_string_from_item, data)
        data.reverse()
        self.sorted_route_table = data
    
    def match(self, req_domain, req_port):
        matched_app = None
        for spec, (domain_pat, domain, port, app) in self.sorted_route_table:
            if domain:
                if domain_pat.match(req_domain):
                    if port:
                        if port == req_port:
                            matched_app = app
                            break
                        else:
                            continue
                    else:
                        matched_app = app
                        break
                else:
                    continue
            else:
                if port:
                    if port == req_port:
                        matched_app = app
                        break
                    else:
                        continue
                else:
                    matched_app = app
                    break
        return matched_app
        
    def __call__(self, environ, start_response):
        req_domain = environ["HTTP_HOST"].lower()
        req_port = int(environ["HTTP_PORT"])
        matched_app = self.match(req_domain, req_port)
        if matched_app:
            return matched_app(environ, start_response)
        else:
            self.logger.debug("no virtual host match for '%s:%s'" % (req_domain, req_port))
            return self.default(environ, start_response)
        
def make_virtualhost_app(loader, global_conf, default = None, **hosts):
    """
    Paste EGG entry point::
        
        virtualhost
        
    PasteDeploy example::
        
        [app:NotFound]
        use = egg:khan#status
        status = 404
        
        [composite:VirtualHost]
        use = egg:khan#virtualhost
        default = NotFound
        domain1.com = Vhost1
        domain2.com:8080 = Vhost2
        *.domain3.com = Vhost3
        *:* = Vhost4
        *:90 = Vhost5
        
        [composite:Vhost1]
        use = egg:paste#urlmap
        / = app1
    """
    
    vhost_app = VirtualHost(default)
    for domain, app_name in hosts.items():
        if "=" in app_name:
            port, app_name = app_name.split("=")
            rule = domain.strip() + ":" + port.strip()
            app = loader.get_app(app_name.strip())
        else:
            rule = domain
            app = loader.get_app(app_name)
    vhost_app[rule] = app 
    return vhost_app