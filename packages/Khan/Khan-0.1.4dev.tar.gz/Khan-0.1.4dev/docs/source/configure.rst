Khan 项目配置文件
===============================

用过 zope 的朋友都了解 zcml, khan 也使用 ZCML 来配置项目, 以下是个例子::

    <?xml version="1.0" encoding="UTF-8"?>

    <configure xmlns="http://bitbucket.org/khan/khan">
    
        <include package="khan.deploy" file="meta.zcml" />
    
        <default>
            <var name="package">myproject</var>
            <var name="here">/path/to/myproject</var>
        </default>
    
        <deployment>
            
            <!-- 指定 wsgi 服务器, 这里可以 -->
            <server use="egg:Paste#http" app="main" />
           
            
            <!-- 日志配置 -->
            <logging keys="root" level="debug">
                <logger name="root" handlers="console" />
                <handler name="console" level="debug" cls="logging.StreamHandler"
                    formatter="colored" />
                <!-- 使用 Khan 提供的多彩日志, 在控制台上输出是高亮多彩的 -->
                <formatter name="colored" cls="khan.deploy.logging.ColorFormatter" />
            </logging>
    
            <composite name="main" use="egg:Paste#cascade">
                <param name="app1">static</param>
                <param name="app2">example</param>
            </composite>
    
            <app name="static" use="egg:Khan#static">
                <param name="document_roots">%(here)s/%(package)s/public</param>
            </app>
            
            <filter name="example" use="egg:Khan#session" next="example_app" />
            
            <app name="example_app" handler=".example.index" />
    
        </deployment>
    
    </configure>

default 指令
------------------------------

定义一些变量, 这些变量可以在配置文件里面使用, 也会附加到 `make_X` 函数的第一个参数 `global_conf` 字典里

实例1::
    
    <default>
        <var name="here">/path/to/myproject</var>
    </default>
    
    <server maker="myproject.server:make_server" app="main">
        <param name="cachedir">%(here)s/data/cache</param>
    </server>
    
server 指令
------------------------------

指定使用哪一个 wsgi 服务器, 如不提供该指令则默认使用 paste 的 http 多线程服务器.

实例1::
    
    <server use="egg:Paste#http" app="main" />
    
实例2::
    
    <server use="egg:cogen#http" pipeline="session cache main" />
    
实例3::
    
    <server use="egg:Paste#http" app="main">
        <param name="host">10.0.0.2</param>
        <param name="port">8080</param>
    </server>
  
实例3::
    
    <server maker="myproject.myserver:make_server" app="main">
        <param name="host">10.0.0.2</param>
        <param name="port">8080</param>
    </server>
    
指令参数/属性说明:
    
    1. `use`
        
        指定 wsgi server
        
        用法:
        
        * use="egg:Paste#http"
        * use="config:/path/to/other_conf.zcml#http"
        * use="ref:other_server_section_name"
        
        .. note::
        
            `use` 和 `maker` 只能选其一, 并且两个必须提供一个
            
    2. `maker`
        
        指定一个函数去建立 wsgi server
        
        用法:
        
        * maker="myproject.myserver:make_server"
    
    3. `app`
        
        指定 wsgi app 名, app 名来自 ``app``/``filter``/``composite`` 指令, 后面会有介绍
        
        用法:
        
        * app="myapp"
    
    4. `pipeline`
        
        指定一个 wsgi app 序列
        
        用法:
        
        * pipeline="sesssion_middleware cache_middleware myapp"
        
        .. note::
        
            `app` 和 `pipeline` 只能选其一, 并且两个必须提供一个

logging 指令
------------------------------

配置服务器日志

实例1::
    
    <logging keys="console other" level="debug">
        <logger name="root" handlers="console" />
        <handler name="console" level="debug" cls="logging.StreamHandler"
            formatter="colored" />
        <formatter name="colored" cls="khan.deploy.logging.ColorFormatter" />
        <logger name="other" handlers="myhandler" />
        <handler name="myhandler" level="debug" cls="logging.StreamHandler"
            formatter="default" />
        <formatter name="default" cls="logging.Formatter" />
    </logging>
    
filter 指令
------------------------------

定义中间件

实例1::

    <filter name="example" use="egg:Khan#session" next="example_app" />
    <app name="example_app" handler=".example.index" />
    
实例2::

    <filter name="example" maker="myproject.session:make_session_middleware" next="example_app">
        <param name="p1">1</param>
        <param name="p2">2</param>
    </filter>
    <app name="example_app" handler=".example.index" />
    
app 指令
------------------------------

定义 app

实例1::

    <app name="example_app" handler=".example.index" />
    
实例2::
    
    <filter name="session" use="egg:Khan#session" />
    <app name="example_app" maker=".example.make_app" filter="session" />
        <param name="p1">1</param>
        <param name="p2">2</param>
    </filter>

composite 指令
------------------------------

同样是定义 app

实例1::

    <composite name="main" use="egg:Paste#cascade">
        <param name="app1">static</param>
        <param name="app2">example</param>
    </composite>

include 指令
------------------------------

包含其他的配置文件, 支持相对路径

实例1::
    
    <include package="myproject" file="app_defines.zcml" />
