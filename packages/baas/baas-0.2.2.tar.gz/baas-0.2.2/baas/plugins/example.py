# -*- coding: utf-8 -*-
# Copyright 2009 Martin Borho <martin@borho.net>
# GPL - see License.txt for details
from baas.core.plugins import Plugin
from baas.core.helpers import strip_tags, xmlify

class Example(Plugin):

    def __init__(self, config, format='xmpp'):
        # call parent init
        super(Example,self).__init__(config, format)
        # set plugin related instance variables
        self.blafasel = None
        
    def get_map(self):
        """
            returns the command map for the plugin
        """
        cmd_map = [('example',self.example_action)]
        return cmd_map

    def get_help(self):
        """
            returns the help text for the plugin
        """
        return {'commands':['example:foo - gives you a bla for a foo'],'additional':[]}

    def example_action(self, term):
        '''
        example plugin
        '''
        result = ''
        term = term.strip()
        if term == '':
            return "Please specify your term"

        if term != 'foo':
            text = "I don't understand...?"
        else:
            text = "bla"

        return self.render(data=text, title=None)

    def render_xmpp(self, data, title):
        #result = title+"\n" #Would be the title
        result = data
        return strip_tags(result)

    def render_wave(self, data, title):
        #Would be the title
        result = " <br/><br/>" #<b>%s</b><br/>" % self.xmlify(title)
        result += "<b>%s</b>" % xmlify(data)
        return result