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
from trac.wiki.macros import WikiMacroBase
from trac.wiki.formatter import system_message

from ohloh_widgets.lib.attribute_dict import AttrDict

__all__ = ['MacroWithValidation']


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

