# encoding: utf-8
#
# sk.recipe.xdv implementation
# 
# Copyright 2010 Sean Kelly and contributors.
# This is licensed software. Please see the LICENSE.txt file for details.

'''XDV compiler recipe for Buildout: implementation.'''

import logging, os, os.path, zc.buildout, xdv.compiler, xdv.utils

_truthiness = ('true', 'yes', '1')
_defaultIncludeMode = 'document'

class Recipe(object):
    '''This is a Buildout recipe that compiles XDV rules and themes into XSLT using the XDV compiler.'''
    def __init__(self, buildout, name, options):
        '''Initialize the recipe.'''
        self.buildout, self.name, self.options, self.logger = buildout, name, options, logging.getLogger(name)
        
        # Check options: *both* rules and theme are required at a minimum.
        if 'rules' not in options:
            raise zc.buildout.UserError('No ``rules`` option specified to XDV recipe; ``rules`` is required')
        if 'theme' not in options:
            raise zc.buildout.UserError('No ``theme`` option specified to XDV recipe; ``theme`` is required')
        
        # The compiled XSLT defaults to buildout/parts/part-name/theme.xsl, but can be overridden:
        if 'output' not in options:
            options['output'] = os.path.join(buildout['buildout']['parts-directory'], name, 'theme.xsl')
        
        # Default the includemode if not given:
        options['includemode'] = options.get('includemode', _defaultIncludeMode)
        
        # Check if network access is allowed:
        if 'network' in options:
            self.networkOK = options['network'].lower() in _truthiness
        else:
            self.networkOK = buildout['buildout']['offline'].lower() not in _truthiness
    
    def install(self):
        '''Compile XDV.'''
        gen = xdv.compiler.compile_theme(
            self.options['rules'],
            self.options['theme'],
            includemode=self.options['includemode'],
            access_control=self.networkOK and xdv.utils.AC_READ_NET or xdv.utils.AC_READ_FILE
        )
        try:
            os.makedirs(os.path.dirname(self.options['output']))
        except OSError:
            pass
        gen.write(self.options['output'], encoding='utf-8')
        self.options.created(self.options['output'])
        return self.options.created()
    
    def update(self):
        '''Update the XDV. Since the theme or the rules (or anything it XIncludes) may change, we re-do the install.'''
        return self.install()
    
    # No custom uninstall required
    
