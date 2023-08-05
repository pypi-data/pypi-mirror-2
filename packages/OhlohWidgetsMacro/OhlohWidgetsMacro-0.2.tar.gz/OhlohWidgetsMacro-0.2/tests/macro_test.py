
from trac.test import EnvironmentStub

from ohloh_widgets.macro import OhlohWidgetMacro, OhlohWidgetParameters
from ohloh_widgets.lib.attribute_dict import AttrDict
from ohloh_widgets.lib.testcase import PythonicTestCase


class OhlohWidgetMacroTest(PythonicTestCase):
    
    def setUp(self):
        self.env = EnvironmentStub(enable=('ohloh_widgets.macro.ohlohwidgetmacro',))
        self.macro = OhlohWidgetMacro(self.env)
    
    # --- Helpers --------------------------------------------------------------
    
    def parse_arguments(self, input):
        parameters, error = self.macro.validate_arguments(OhlohWidgetParameters(), input)
        return parameters, error
    
    def assert_valid_arguments(self, input):
        parameters, error = self.parse_arguments(input)
        self.assert_none(error)
        return (parameters.project_id, parameters.widget_name)

    
    def assert_invalid(self, input):
        parameters, error = self.parse_arguments(input)
        self.assert_none(parameters)
        self.assert_not_none(error)
        return error
    
    # --- validation tests -----------------------------------------------------
    
    def test_can_split_positional_arguments(self):
        self.assert_equals((123456, 'foo'), self.assert_valid_arguments('123456, foo'))
    
    def test_validation_fails_if_no_arguments_given(self):
        self.assert_invalid(None)
    
    def test_validation_fails_if_project_id_is_not_numeric(self):
        self.assert_invalid('abc, foo')
    
    def test_validation_fails_if_widget_name_is_missing(self):
        self.assert_invalid('1234')
    
    # --- script url tests -----------------------------------------------------
    
    def test_generates_correct_script_url(self):
        url = self.macro.url(AttrDict(project_id=123, widget_name='foo'))
        self.assert_equals('http://www.ohloh.net/p/123/widgets/foo.js', url)
    
    def test_supports_query_parameters(self):
        url = self.macro.url(AttrDict(project_id=123, widget_name='foo?q=bar'))
        self.assert_equals('http://www.ohloh.net/p/123/widgets/foo.js?q=bar', url)

