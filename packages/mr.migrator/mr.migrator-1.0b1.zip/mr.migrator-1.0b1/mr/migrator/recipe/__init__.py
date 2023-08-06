# -*- coding: utf-8 -*-
"""Recipe mr.migrator"""

from zc.recipe.egg.egg import Scripts
from urllib import pathname2url as url
from sys import argv
import logging
from pkg_resources import resource_string, resource_filename


logging.basicConfig(level=logging.DEBUG)

class Recipe(Scripts):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        args = {}
        for k,v in self.options.items():
            if '-' in k:
                part,key = k.split('-',1)
                args.setdefault(part, {})[key] = v
        default = buildout['buildout']['directory']+'/var/cache'
        
        self.options['scripts'] = 'migrate=%s'%name

        self.options['eggs'] = """
                mr.migrator
                """ + self.options.get('eggs','')
        pipeline = self.options['pipeline']
        if ':' in pipeline:
            package, pipeline_name = pipeline.split(':')
            self.options['eggs'] += "  %s"%package

        pipeline = self.options.get('pipeline',None)
        if pipeline:
            self.options['arguments'] =  str(args)+',"'+pipeline+'"'
        else:
            self.options['arguments'] =  str(args)
        return  Scripts.__init__(self, buildout, name, options)

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here




        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return Scripts.install(self)

    def update(self):
        """Updater"""
        return Scripts.update(self)
