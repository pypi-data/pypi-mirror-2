.. _index:

***************************************************
:mod:`khan` -- WSGI 基础框架
***************************************************

:Author: timbaby2008@gmail.com
:Version: |version|

.. module:: khan
   :synopsis: WSGI 常用应用程序与中间件工具集

概述
==============================

:mod:`khan` 是一个 *Python WSGI* 工具库，提供了若干常用的 *Application* 和 *Middleware*, 
旨在使用户通过简单地编辑配置文件就可以部署好自己的 WSGI 服务器, 使用 Khan 可以提升您的网站开发效率.

特性
==============================

* 安装部署简便, :doc:`灵活简洁的 XML 配置文件 <configure>`
* 符合 WSGI 标准, 你只需要提供一个标准的 WSGI APP, Khan 就可以帮你运行它
* 可随意更换 WSGI 服务器(默认使用 paste 的多线程 http 服务器)
* 丰富的文档, 方便参与开发
* 内置很多常用的基本组件

    * :doc:`静态文件服务 <modules/static>`
    * :doc:`压缩与文件最优化支持 <modules/compress>`
    * :doc:`URL 分发与过滤 <modules/urlparse>`
    * :doc:`虚拟主机支持 <modules/virtualhost>`
    * :doc:`HTTP 状态处理 <modules/httpstatus>`
    * :doc:`错误文档 <modules/error_document>`
    * :doc:`代理/透明代理 <modules/proxy>`
    * :doc:`用户会话管理 <modules/session>`
    * :doc:`缓存支持 <modules/cache>`
    * :doc:`事件通知与广播 <modules/notification>`
    * :doc:`JSON 工具与 JSONRPC 服务 <modules/json>`
    * :doc:`安全与身份验证 <modules/security>`
    * :doc:`控制器实现 <modules/controller>`
    * :doc:`数据转换与校验 <modules/schema>`
    * :doc:`简单存储 <modules/store>`
    * :doc:`常用工具 <modules/utils/index>`
    * :doc:`命令行支持 <modules/command>`

更多请参阅: `官方网站 <http://bitbucket.org/khan/khan>`_ 

为什么叫 Khan ?
==============================

**Khan** 意为 ``可汗``, 是一个很有中国特色的名词，中国北朝时期的柔然族，唐朝时期的回纥族、突厥族和宋元时期的蒙古族，
称首领为 ``可汗``. 

(其实是因为我当时想来想去想不到有特色的名词, 小动物名字都让各种项目用了, 冏~~, 我承认, Khan 这名字是起大了 -_-P)

如何贡献?
==================

khan 是一个非常年轻的项目, 还不够完善, 本人也是业余时间来开发他, 我希望能有更多的朋友参与共同开发, 使他更快的完善, 
成为一个足够好用的, 可以在生产环境部署的纯 WSGI 框架.

如果你有兴趣参与, 请给我邮件 ^_^ timbaby2008@gmail.com

环境依赖
===============================

1. Python2.6
2. setuptools 包 (如果你可以使用 `easy_install` 命令就意味已经安装了)

下载及安装
===============================

从仓库检出源代码::

    hg clone https://bitbucket.org/khan/khan

或直接通过 easy_install 安装开发版本::

    $ sudo easy_install http://bitbucket.org/khan/khan/get/tip.tar.gz

部署和配置
===============================

建立一个项目::
    
    $ paster create -t khan.starter myproject

运行该项目::
    
    $ cd myproject
    $ ./devserver.sh (Windows 不支持)
    
或者::
    
    $ paster khan.serve --reload -p myproject

打开浏览器, 输入网址即可访问到新建的  Project::

    http://localhost:7010 
    
调试项目
==================

Khan 包含了一个 ``nose`` 的插件, 支持用 ``nose`` 进行测试, 运行实例::
    
    $ python setup.py test
    
    **********************************************************************
    Loading Khan project environ ...
    **********************************************************************
    
    test_example (myproject.tests.test_example.TestAll) ... ok
    
    **********************************************************************
    Closed Khan project environ.
    **********************************************************************
    
    
    ----------------------------------------------------------------------
    Ran 1 test in 0.049s
    
    OK

Khan 还包含了一个叫 `khan.shell` 的小程序, 可以方便地调试你的项目, 推荐 Linux 下的话先安装 **bpython**, 
如果你安装了 bpython 的话, `khan.shell` 将会使用他作为 shell::
    
    $ paster khan.shell -p myproject
    
    >>> app
    <paste.fixture.TestApp object at 0x2e8ce10>
    >>> app.get("/")
    <Response 200 OK 'Hello world!'>
    >>> app.post("/")
    <Response 200 OK 'Hello world!'>
    >>> resp = app.post("/")
    >>> resp.status_int
    >>> resp.status
    200

部署运行其他应用/框架
===============================

* :doc:`Django <deploy/django>`
* :doc:`webpy <deploy/webpy>`
