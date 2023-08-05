# -*- coding: UTF-8 -*-
#
# The MIT License
# 
# Copyright (c) 2010 Felix Schwarz <felix.schwarz@oss.schwarz.eu>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from genshi.builder import tag
from trac.core import Component, implements

from ohloh_widgets.api import IOhlohWidgetModifier

__all__ = ['ProjectBasicStats', 'ProjectFactoids']


class ProjectBasicStats(Component):
    implements(IOhlohWidgetModifier)
    
    def widget_name(self):
        return "project_basic_stats"
    
    def widget_fix(self, tag_id):
        ""
        js = '''
            var widget = jQuery('#%(tag_id)s');
            
            // trac's wiki page/h3 has a negative margin-left
            widget.find('h3').css({'margin-left': '-10px'});
            
            // #div.gadget div.main' gets an additional margin-left which looks
            // bad - however it's done with an addition <style> tag so we can't
            // remove the rule itself. Instead this will make sure that the rule
            // does not apply anymore
            widget.find('div.gadget div.main').removeClass('main');
            
            // the Ohloh logo floats all the way to the right, so we just set
            // a width
            widget.find('div.gadget').css({'width': '20em'});
        ''' % dict(tag_id=tag_id)
        return tag.script(js, type='text/javascript')


class ProjectFactoids(Component):
    implements(IOhlohWidgetModifier)
    
    def widget_name(self):
        return "project_factoids"
    
    def widget_fix(self, tag_id):
        ""
        js = '''
            var factoid = jQuery('#%(tag_id)s');
            var factoidDivElements = factoid.find('div');
            
            // remove background color
            var factoidWithBackgroundColor = function(index){ return 'transparent' !== jQuery(this).css('background-color'); };
            factoidDivElements.filter(factoidWithBackgroundColor).css('background-color', 'transparent');
            
            // remove round corners
           factoidDivElements.filter(function() { return "none" !== $(this).css('background-image') }).remove()
           
           // ensure all links have the right color
           factoid.find('a').css({'color': null}); 
        ''' % dict(tag_id=tag_id)
        return tag.script(js, type='text/javascript')

