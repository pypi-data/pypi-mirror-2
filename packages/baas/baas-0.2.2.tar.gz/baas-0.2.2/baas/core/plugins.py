# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
import os
import new
import re
from baas import plugins
from baas.core.helpers import strip_tags, xmlify, htmlentities_decode, load_url, load_feed


class PluginLoader(object):

    def __init__(self, config=None, format='xmpp'):
        self.config = config
        self.format = format
        self.plugins = {}
        self.help = ''
        self.commands = {}
        self.limits = {}

    def load_plugins(self):
        """
            loads the plugins from the plugin dir
        """
        for file in os.listdir(plugins.__path__[0]):
            file_parts = os.path.splitext(file)
            if  file_parts[1] == '.py' and file[0:2] != '__':
                self.plugins[file_parts[0].capitalize()] = \
		getattr(__import__('baas.plugins.'+file_parts[0], globals(), \
		locals(),[file_parts[0].capitalize()]), \
		file_parts[0].capitalize())(config=self.config, format=self.format)

    def load_map(self):
        """
            combines command map
        """
        for name in self.plugins:
            cmd_map = self.plugins[name].get_map()
            if cmd_map:
                for (cmd,func) in cmd_map:
                    self.commands[cmd] = func

    def load_limits(self):
        """
            combines command map
        """
        for name in self.plugins:
            limit_map = self.plugins[name].get_limits()
            if limit_map:
                for (cmd,limit) in limit_map:
                    self.limits[cmd] = limit
                    
    def load_help(self):
        """
            combines help text, retrieved from the plugins
        """
        help_infos = {}
        help_list = []
        help_additional = []
        for name in self.plugins:
            help_info = self.plugins[name].get_help()
            if help_info:
                help_infos[name] = help_info

        for h in help_infos:
            for t in help_infos[h].get('commands'):
                help_list.append(t)
            for a in help_infos[h].get('additional',[]):
                if a: help_additional.append(a)

        self.help = "\n".join(help_list)
        self.help += "\n\n%s" % "\n\n".join(help_additional)           
        
class Plugin(object):

    def __init__(self, config, format='xmpp'):
        self.config = config
        self.format = format
        self.result_limit = None

    def get_map(self):
        return None

    def get_limits(self):
        return None

    def get_help(self):
        return None

    def extract_page_param(self, term):
        """
            extract optional page paramter from term
        """
        page = 1
        pgrep = re.search('.*\[([0-9]+)\][^\]]*$', term)
        if pgrep:
            page_num = int(pgrep.group(1))
            term = term.replace('[%d]' % page_num,'').strip()
            if page_num > 0:
                page = page_num
        return (term, page)

    def strip_tags(self, value):
        """
            Return the given HTML with all tags stripped.
        """
        return strip_tags(value)        

    def xmlify(self, string):
        """
           makes a string xml valid
        """
        return xmlify(string)

    def htmlentities_decode(self, string):
        """ 
            decodes htmlentities 
        """
        return htmlentities_decode(string)

    def render(self, data, title='', extra_format=None):
        """ 
            chooses the right render function, returns raw dict direct 
        """
        if self.format == "raw":
            return data
            
        render_func = 'render_'+self.format
        if extra_format:
            render_func += '_'+extra_format
        return  getattr(self, render_func)(data, title)

    def render_xmpp(self, data):
        pass

    def render_wave(self, data):
        pass
