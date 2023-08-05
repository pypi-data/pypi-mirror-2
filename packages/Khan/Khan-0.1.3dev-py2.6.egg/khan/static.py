# -*- coding: utf-8 -*-

"""
静态文件服务
=================================

本模块提供工具去服务静态文件.

.. TODO::
    
    * 大文件优化
    * linux sendfile() 支持
    
索引
=================================

* :class:`File`
* :class:`Static`
* :class:`StaticDirectory`
* :class:`StaticCommand`
* :func:`make_file_app`
* :func:`make_static_app`
    
=================================

.. autoclass:: File
.. autoclass:: Static
.. autoclass:: StaticDirectory
.. autoclass:: StaticCommand
.. autofunction:: make_file_app
.. autofunction:: make_static_app
"""

import logging, os, platform
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from paste.deploy import converters
from paste.fileapp import FileApp
from paste.httpserver import serve
from paste.httpheaders import LAST_MODIFIED
from khan.utils import isiterable
from khan.command import Command, BadCommand
from khan.deploy import loadobject

CACHE_SIZE = 4096
BLOCK_SIZE = 4096 * 16

logger = logging.getLogger( __name__ )

__all__ = ["Static", "StaticDirectory", "File"]

if platform.system().lower() in ["unix", "linux"]:
    EX_OK = os.EX_OK
else:
    EX_OK = 0
    
class File(FileApp):
    """
    服务一个单一静态文件
    """
    
    def __init__(self, file, headers = [], content_type = None, content_encoding = None):
        """
        :param file: 文件名或文件对象
        :param content_type: content type, 当不提供的时候会自动检测
        :param content_encoding: content encoding, 当不提供的时候会自动检测
        :param headers: http 头, [(key, value)] 形式
        """
        
        if isinstance(file, basestring):
            file = os.path.abspath(file)
            filename = file
        else:
            # FIXME ZODB的BlobFile open出来的对象无法写入name属性，暂时使用filename替代
            if hasattr( file, 'filename' ):
                filename = file.filename
            else:
                filename = file.name

        kwargs = {}
        if content_type:
            kwargs["content_type"] = content_type
        if content_encoding:
            kwargs["content_encoding"] = content_encoding

        self.filename = filename
        self.file = file
        content_type, content_encoding = self.guess_type()
        if content_type and 'content_type' not in kwargs:
            kwargs['content_type'] = content_type
        if content_encoding and 'content_encoding' not in kwargs:
            kwargs['content_encoding'] = content_encoding

        FileApp.__init__(self, filename, headers, **kwargs)
    
    def _apply_content_disposition_header(self, filename):
        fname = os.path.basename(filename)
        if isinstance(fname, unicode):
            fname = fname.encode("utf-8", "ignore")
        self.headers.append(("Content-Disposition", "attachment; filename=\"%s\"" % fname))
    
    def update(self, force=False):
        if os.path.isfile( self.filename ):
            stat = os.stat(self.filename)
            if not force and stat.st_mtime == self.last_modified:
                return
            self.last_modified = stat.st_mtime
            if stat.st_size < CACHE_SIZE:
                fh = open(self.filename,"rb")
                self.set_content(fh.read(), stat.st_mtime)
                fh.close()
            else:
                self.content = None
                self.content_length = stat.st_size
                # This is updated automatically if self.set_content() is
                # called
                LAST_MODIFIED.update(self.headers, time=self.last_modified)

        elif hasattr( self.file, 'read' ):
            # FIMXE 强制检查无效
            if force:
                self.content = None
                logger.warn( 'static file like object not supported force refresh' )

            #if self.content:
            #    return

            try:
                self.file.seek( 0 )
                self.set_content( self.file.read() )

                if hasattr( self.file, 'close' ) and callable( self.file.close ):
                    self.file.close()
            except IOError:
                logger.error( 'static file read failed', exc_info=True )

            for method in [ 'len', '__len__' ]:
                if hasattr( self.file, method ) and callable( getattr( self.file, method ) ):
                    self.content_length = getattr( self.file, method )()
            else:
                self.content_length = len( self.content )

    def __call__(self, environ, start_response):
        headers_dict = dict(self.headers)
        content_type = headers_dict.get("Content-Type")
        if not content_type:
            self._apply_content_disposition_header(self.filename)
        elif content_type == "application/octet-stream":
            self._apply_content_disposition_header(self.filename)
    
        return super(File, self).__call__(environ, start_response)
        
def make_file_app(global_conf, file, headers = None,  content_type = None, 
                  content_encoding = None, conf = None):
    """
    Paste EGG entry point::
        
        file
        
    PasteDeploy example::
    
        [app:FileApp]
        use = egg:khan#file
        file = /home/alec/kk.py
        headers = extra_headers
        
        [object:extra_headers]
        use = egg:khan#dict
        X-Kh-Sid = 123456
    """
    
    config_file = conf or global_conf["__file__"]
    h = []
    if headers:
        for name in headers.split():
            for header_key, value in loadobject("config:%s" % config_file, name, global_conf).items():
                h.append((header_key, value))
    app = File(file, headers = h, content_type = content_type, content_encoding = content_encoding)
    return app

class StaticDirectory(StaticURLParser):
    
    def make_app(self, filename):
        return File(filename)
    
class Static(object):
    """
    服务一个或者多个目录下的静态文件, Static 将请求的 url 映射为目录下的文件路径，
    如果是服务多个目录，那么 Static 将按顺序在所有目录下寻找对应的文件，一旦在任
    一个目录下找到相应的文件则停止搜索并返回该文件内容.
    """
    
    def __init__(self, document_roots, cache_max_age = None):
        """
        :param document_roots: 目录列表
        :param cache_max_age: integer specifies Cache-Control max_age in seconds 
        
        :type document_roots: list
        """
        
        if not isiterable(document_roots):
            document_roots = [document_roots]
        if len(document_roots) == 1:
            self._app = StaticDirectory(document_roots[0], cache_max_age = cache_max_age)
        elif len(document_roots) > 1:
            self._app = Cascade([StaticDirectory(dir, cache_max_age = cache_max_age) for dir in document_roots])
        else:
            raise ValueError("`document_roots` invalid")
        
    def __call__(self, environ, start_response):
        return self._app(environ, start_response)
        
def make_static_app(global_conf, document_roots, cache_max_age = None):
    """
    Paste EGG entry point::
        
        static
        
    PasteDeploy example::
    
        [app:StaticApp]
        use = egg:khan#static
        document_roots = /etc /home/alec
    """
    
    dirs = filter(lambda item: item.strip(), converters.aslist(document_roots))
    cache_max_age = cache_max_age and int(cache_max_age) or None
    app = Static(dirs, cache_max_age = cache_max_age)
    return app

class StaticCommand(Command):
    """
    Serve static file or dir.
    
    Example::
    
        $ paster khan.static /etc/passwd
    """
    
    args_description = "file_or_dir"
    
    min_args = 1
    
    max_args = 1
    
    parser = Command.standard_parser(simulate=True)
    
    parser.add_option('-s', '--server',
                      dest='host',
                      default = "0.0.0.0",
                      help="host. [default: %default]")
    
    parser.add_option('-p', '--port',
                      dest='port',
                      default="7010",
                      help="port. [default: %default]")
    
    def command(self):
        file = self.args[0]
        file = os.path.abspath(file)
        if os.path.isfile(file):
            app = File(file)
        elif os.path.isdir(file):
            app = Static(file)
        else:
            raise BadCommand("no such file or dir '%s'." % file)
        serve(app, host=self.options.host, port=int(self.options.port))
        return EX_OK
