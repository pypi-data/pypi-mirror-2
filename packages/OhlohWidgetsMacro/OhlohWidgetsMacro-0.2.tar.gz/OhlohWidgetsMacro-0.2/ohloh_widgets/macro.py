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
from pycerberus import Validator
from pycerberus.validators import IntegerValidator, StringValidator
from trac.core import ExtensionPoint

from ohloh_widgets.api import IOhlohWidgetModifier
from ohloh_widgets.util import MacroWithValidation
from ohloh_widgets.validation import CommaSeparatedArgumentsParsingSchema, VarArgsParsingSchema


class OhlohWidgetParameters(CommaSeparatedArgumentsParsingSchema):
    
    parameter_order = ('project_id', 'widget_name')
    project_id = IntegerValidator()
    widget_name = StringValidator()


class OhlohWidgetMacro(MacroWithValidation):
    """Macro to embed Ohloh widgets in wiki pages.
    
    Example:
       ![[OhlohWidget(project_id, widget_name)]]
    
    The macro gets two parameters which you can get from Ohloh's widget page
    for your project (!http://www.ohloh.net/p/<project name>/widgets) when you
    look at the embeddable HTML snippet:
    
     * project_id -- a 6 digit number which identifies your project
     * widget_name -- the Javascript filename with the '.js' suffix (e.g. "project_factoids")
    
    """
    
    modifiers = ExtensionPoint(IOhlohWidgetModifier)
    
    # ---- WikiMacroBase public methods ----------------------------------------
    
    def expand_macro(self, formatter, macro_name, argument_string, processor_parameters=None):
        parameters, error = self.validate_arguments(OhlohWidgetParameters(), argument_string)
        if error:
            return self.show_all_errors(error)
        
        widget_tag = self._script_tag_for_widget(parameters)
        return self._container_for_widget(parameters, widget_tag)
    
    # ---- HTML generation -----------------------------------------------------
    
    def url(self, parameters):
        query_string = ''
        url_template = 'http://www.ohloh.net/p/%(project_id)d/widgets/%(widget_name)s.js'
        widget_name = parameters.widget_name
        if '?' in widget_name:
            parameters['widget_name'], query_parameters = widget_name.split('?', 1)
            query_string = '?' + query_parameters
        return (url_template % parameters) + query_string
    
    def _script_tag_for_widget(self, parameters):
        script_url = self.url(parameters)
        return tag.script(src=script_url, type='text/javascript')
    
    def _widget_modification(self, widget_name, tag_id):
        for modifier in self.modifiers:
            if modifier.widget_name() == widget_name:
                return modifier.widget_fix(tag_id)
        return None
    
    def _container_for_widget(self, parameters, widget):
        tag_id = 'ohloh-%(project_id)d-%(widget_name)s' % parameters
        modification = self._widget_modification(parameters.widget_name, tag_id)
        css_classes = ['ohloh-widget', parameters.widget_name]
        return tag.span(widget, modification, id=tag_id, class_=' '.join(css_classes))



class OhlohWidgetGroupParameters(VarArgsParsingSchema):
    
    parameter_order = ('project_id', 'widget_names')
    project_id = IntegerValidator()
    widget_names = Validator()


class OhlohWidgetGroup(MacroWithValidation):
    """Macro to embed a group of Ohloh widgets in wiki pages.
    
    Example:
       ![[OhlohWidgetGroup(project_id, first_widget_name, second_widget_name)]]
    
    The parameter values are the same as for the !OhlohWidget macro.
    
    This macro will put all contained widgets in a div element which you can
    style easily with CSS.
    """
    
    # ---- WikiMacroBase public methods ----------------------------------------
    
    def expand_macro(self, formatter, macro_name, argument_string, processor_parameters=None):
        parameters, error = self.validate_arguments(OhlohWidgetGroupParameters(), argument_string)
        if error:
            return self.show_all_errors(error)
        
        widgets = self._widget_tags(parameters, formatter, macro_name)
        return self._container_for_widget(parameters, widgets)
    
    def _widget_tags(self, parameters, formatter, macro_name):
        widgets = []
        macro = OhlohWidgetMacro(self.env)
        for widget_name in parameters.widget_names:
            widget_paremeters = dict(project_id=parameters.project_id, widget_name=widget_name)
            argument_string = '%(project_id)s, %(widget_name)s' % widget_paremeters
            widget = macro.expand_macro(formatter, macro_name, argument_string)
            widgets.append(widget)
        return widgets
    
    def _container_for_widget(self, parameters, widgets):
        parameters['widget_names'] = '-'.join(parameters.widget_names)
        tag_id = 'ohloh-%(project_id)d-%(widget_names)s' % parameters
        return tag.div(widgets, id=tag_id, class_='ohloh-widgets')

