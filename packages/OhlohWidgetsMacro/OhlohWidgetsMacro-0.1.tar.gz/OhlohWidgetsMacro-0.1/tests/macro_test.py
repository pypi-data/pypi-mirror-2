
from pycerberus import InvalidDataError
from trac.test import EnvironmentStub

from ohloh_widgets.macro import OhlohWidgetMacro, OhlohWidgetParameters
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
    
    # --- Tess -----------------------------------------------------------------
    
    def test_can_split_positional_arguments(self):
        self.assert_equals((123456, 'foo'), self.assert_valid_arguments('123456, foo'))
    
    def test_validation_fails_if_no_arguments_given(self):
        self.assert_invalid(None)
    
    def test_validation_fails_if_project_id_is_not_numeric(self):
        self.assert_invalid('abc, foo')
    
    def test_validation_fails_if_widget_name_is_missing(self):
        self.assert_invalid('1234')

