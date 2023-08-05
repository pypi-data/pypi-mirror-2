# -*- coding: utf-8 -*-

import os, sys
from paste.script.templates import var
from core import ProjectTemplate

class DjangoTemplate(ProjectTemplate):
    
    _template_dir = "templates/django"
    summary = "Khan django project"
    
    vars = [
        var('django-admin', 'Path to your "django-admin.py" command', 
            default='django-admin.py')
    ]
    
    def pre(self, command, output_dir, vars):
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        cwd = os.getcwd()
        os.chdir(output_dir)
        sts = os.system(vars['django-admin'] + ' startproject ' + vars['package'])
        os.chdir(cwd)
        if sts != 0:
            sys.exit(sts)
        
            