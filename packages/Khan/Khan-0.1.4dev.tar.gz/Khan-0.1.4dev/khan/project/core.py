# -*- coding: utf-8 -*-

import pkg_resources, sys, os, stat, platform
from paste.script.templates import Template
from paste.script import copydir
from paste.util.template import paste_script_template_renderer
from paste.script.appinstall import Installer

__all__ = ["ProjectTemplate", "ProjectInstaller", "KhanDeployInstaller"]

class ProjectTemplate(Template):
    
    _template_dir = "templates/default"
    summary = "khan base project template"
    template_renderer = staticmethod(paste_script_template_renderer)
    
    def write_files(self, command, output_dir, vars):
        # 增加一个 output_dir 的模板变量
        vars.setdefault("output_dir", os.path.abspath(output_dir))
        return super(ProjectTemplate, self).write_files(command, output_dir, vars)
    
    def post(self, command, output_dir, vars):
        base_template_dir = os.path.join(os.path.dirname(__file__), "templates", "bases")
        copydir.copy_dir(base_template_dir, output_dir,
                         vars,
                         verbosity=command.verbose,
                         simulate=command.options.simulate,
                         interactive=command.interactive,
                         overwrite=command.options.overwrite,
                         indent=1,
                         use_cheetah=self.use_cheetah,
                         template_renderer=self.template_renderer)
        fmode = stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR
        os.chmod(os.path.join(output_dir, "devserver.sh"), fmode)
        if command.verbose:
            print '*' * 72
            print '* Go to `%s` project directory' % vars["package"]
            print '* Run "paster khan.serve --reload %s"' % vars["package"]
            if platform.system() != "Windows":
                print '  - OR -'
                print '  Run "./devserver.sh" to run the application'
            print '* Server on http://localhost:7010'
            print '*' * 72
            
class ProjectInstaller(Installer):
    
    use_cheetah = False
    
    def config_file(self, command, vars):
        return vars["requirement"] + ".ini_tmpl"
    
    def config_content(self, command, vars):
        """
        Called by ``self.write_config``, this returns the text content
        for the config file, given the provided variables.
        """
        
        config_file = self.config_file(command, vars)
        modules = [line.strip()
                    for line in self.dist.get_metadata_lines("top_level.txt")
                    if line.strip() and not line.strip().startswith("#")]
        if not modules:
            print >> sys.stderr, "No modules are listed in top_level.txt"
            print >> sys.stderr, \
                "Try running python setup.py egg_info to regenerate that file"
        for module in modules:
            if pkg_resources.resource_exists(module, config_file):
                return self.template_renderer(
                    pkg_resources.resource_string(module, config_file),
                    vars, filename=config_file)
        # Legacy support for the old location in egg-info
        return super(ProjectInstaller, self).config_content(command, vars)

class KhanDeployInstaller(ProjectInstaller):
    
    def config_file(self, command, vars):
        return "configure.zcml_tmpl"
