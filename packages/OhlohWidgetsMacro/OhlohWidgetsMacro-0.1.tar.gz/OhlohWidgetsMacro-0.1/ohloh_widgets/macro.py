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
from pycerberus import InvalidDataError
from pycerberus.validators import IntegerValidator, StringValidator
from trac.core import ExtensionPoint
from trac.wiki.macros import WikiMacroBase
from trac.wiki.formatter import system_message

from ohloh_widgets.api import IOhlohWidgetModifier
from ohloh_widgets.lib.attribute_dict import AttrDict
from ohloh_widgets.validation import CommaSeparatedArgumentsParsingSchema


class OhlohWidgetParameters(CommaSeparatedArgumentsParsingSchema):
    
    parameter_order = ('project_id', 'widget_name')
    project_id = IntegerValidator()
    widget_name = StringValidator()


class MacroWithValidation(WikiMacroBase):
    abstract = True
    
    def validate_arguments(self, schema, argument_string):
        try:
            return AttrDict(schema.process(argument_string)), None
        except InvalidDataError, e:
            return None, e
    
    def show_all_errors(self, e):
        container = tag.span()
        for field_name, error in e.error_dict().items():
            text = u'%s: %s' % (field_name, error.details().msg())
            container.append(system_message(text))
            container.append(tag.br())
        return container


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
            return self._show_all_errors(error)
        
        widget_tag = self._script_tag_for_widget(parameters)
        return self._container_for_widget(parameters, widget_tag)
    
    # ---- HTML generation -----------------------------------------------------
    
    def url(self, parameters):
        url_template = 'http://www.ohloh.net/p/%(project_id)d/widgets/%(widget_name)s.js'
        return url_template % parameters
    
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
        return tag.span(widget, modification, id=tag_id, class_=parameters.widget_name)


