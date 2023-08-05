# -*- coding: utf-8 -*-

"""
命令行支持
=================================

索引
=================================

* :class:`Command`
* :class:`ProjectCommand`
* :class:`ActionDispatcherCommand`

=================================

.. autoclass:: Command
.. autoclass:: ProjectCommand
.. autoclass:: ActionDispatcherCommand
"""

import sys, os, inspect, warnings, logging
from paste.script.command import Command as _Command, BadCommand
from khan.deploy.core import EnvironLoader

__all__ = ["Command", "BadCommand", "ProjectCommand", "ActionDispatcherCommand"]

class CommandMeta(type):
    
    def __init__(cls, name, bases, attrs):
        summary = ""
        usage = ""
        if cls.__doc__:
            lines = cls.__doc__.splitlines()
            for i, line in enumerate(lines):
                if line.strip():
                    summary = line
                    need_strip_num = len(line) - len(line.lstrip())
                    summary = summary.strip()
                    usage = "\n".join(map(lambda l : l[need_strip_num : ], lines[i  + 1: ]))
                    usage = usage.strip()
                    break 
        cls.summary = summary
        cls.usage = usage
        
class Command(_Command):
    """
    命令行命令基类，封装了 ``paste.script.Command``
    
    实现根据类的 __doc__ 属性自动生成命令行的说明, __doc__ 的具体格式如下::
        
        class MyCommand(Command):
            \"""
            The summary string
            
            the usage string
            \"""
    
    :attr:`args_description`
        
        参数说明，如果不设置该属性，则根据 :attr:`max_args` 自动生成 ``arg arg1 arg2`` 这种说明
        
        该属性最终将显示在::
            
            $ command [OPTIONS] *args_description*
    """
    
    __metaclass__ = CommandMeta
    
    group_name = "khan"
    
    args_description = ""
    
    def parse_args(self, args):
        if not self.args_description:
            if self.max_args > 0:
                args_description = " ".join(map(lambda x : "arg" + str(x) if x > 0 else "arg", range(self.max_args)))
            else:
                args_description = ""
        else:
            args_description = self.args_description
        if self.summary:
            self.summary = "\n\n" + self.summary
        if self.usage:
            self.usage = "\n\n" + self.usage
        self.parser.usage = "%%prog [options] %s%s%s" % (
            args_description, self.summary, self.usage)
        self.parser.prog = self._prog_name()
        if self.description:
            desc = self.description
            self.parser.description = desc
        self.options, self.args = self.parser.parse_args(args)
    
    def _prog_name(self):
        return '%s %s' % (os.path.basename(sys.argv[0]), self.command_name)

class ProjectCommand(Command):
    
    min_args = 0
    
    max_args = 0
    
    package = None
    
    zcml = None
    
    server = None
    
    parser = Command.standard_parser(simulate=True)
    
    def parse_args(self, args):
        if self.server is None:
            self.parser.add_option('-s', '--server',
                              dest='server',
                              default="main",
                              help=("Specifie server name in "
                                    "zcml file [default: %default]"))

        if self.package is None and self.zcml is None:
            self.parser.add_option('-p', '--package',
                              dest='package',
                              default=None,
                              metavar='PACKGE',
                              help="Project package.")
            self.parser.add_option('-z', '--zcml',
                              dest='zcml',
                              default=None,
                              metavar='ZCML',
                              help="Project zcml file.")
        return super(ProjectCommand, self).parse_args(args)
        
    def command(self):
        if self.package:
            package = self.package
        elif hasattr(self.options, "package"):
            package = self.options.package
        else:
            package = None
        if self.zcml:
            zcml = self.zcml
        elif hasattr(self.options, "zcml"):
            zcml = self.options.zcml
        else:
            zcml = None
        if not zcml and not package:
            raise BadCommand("You must give a project package or ZCML file")
        server_name = self.options.server
        if package:
            # 附加当前路径到搜索路径中
            sys.path.append(os.getcwd())
            if isinstance(package, basestring):
                __import__(package, globals(), locals(), [], -1)
                package = sys.modules[package]
        if zcml:
            if not os.path.isfile(os.path.abspath(zcml)):
                raise BadCommand("zcml file '%s' not exists." % zcml)
        self.package = package
        self.zcml = zcml
        if not self.verbose:
            warnings.filterwarnings("ignore")
            logging.raiseExceptions = 0 
        env_loader = EnvironLoader(package, zcml, self.verbose, server_name)
        with env_loader as (app, deploy_context):
            return self.execute(app, deploy_context)
            
    def execute(self, app, deploy_context):
        return

class ActionDispatcherCommand(ProjectCommand):
    
    min_args = 1
    
    max_args = None
    
    args_description = "<action> [argument1 argument2 ...]"
    
    class ActionFactory(object): pass
    
    def parse_args(self, args):
        members = inspect.getmembers(self.ActionFactory)
        extra_usage = u""
        for name, obj in members:
            name = name.lower()
            if not name.startswith("_") and callable(obj):
                doc = obj.__doc__
                summary = ""
                usage = ""
                if doc:
                    lines = doc.splitlines()
                    for i, line in enumerate(lines):
                        if line.strip():
                            summary = line.strip()
                            need_strip_num = len(line) - len(line.lstrip())
                            summary = summary.strip()
                            usage = "\n".join(map(lambda l : "    " + l[need_strip_num : ], lines[i  + 1: ]))
                            usage = "    " + usage.strip()
                            break
                    if usage.strip():
                        extra_usage += "  - <%(action)s> %(summary)s\n\n%(usage)s\n\n" % \
                             dict(action = name.upper(), summary = summary, usage = usage)
                    else:
                        extra_usage += "  - <%(action)s> %(summary)s\n\n" % \
                             dict(action = name.upper(), summary = summary)
                else:
                    extra_usage += "  - <%(action)s> \n\n" % dict(action = name.upper())
        if extra_usage:
            extra_usage = "Actions:\n\n" + extra_usage.rstrip()
        self.usage += extra_usage.strip()
        return super(ActionDispatcherCommand, self).parse_args(args)
        
    def execute(self, app, deploy_context):
        if len(self.args) == 0:
            raise BadCommand("Action missing.")
        action = self.args[0].lower()
        args_of_action = self.args[1 :]
        if action.startswith("_"):
            raise BadCommand("Action '%s' invalid" % action)
        factory = self.ActionFactory()
        factory.cmd = self
        factory.app = app
        factory.deploy_context = deploy_context
        if hasattr(factory, action):
            action_method = getattr(factory, action)
            if not callable(action_method):
                raise BadCommand("Action '%s' invalid" % action)
            else:
                
                return action_method(*args_of_action)
        else:
            raise BadCommand("Action '%s' invalid" % action)
        