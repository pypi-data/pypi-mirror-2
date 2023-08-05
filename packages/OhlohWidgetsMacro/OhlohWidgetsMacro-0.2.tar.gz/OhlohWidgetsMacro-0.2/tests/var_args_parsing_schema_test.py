
from pycerberus.api import Validator
from pycerberus.validators import IntegerValidator

from ohloh_widgets.lib.testcase import PythonicTestCase
from ohloh_widgets.validation import VarArgsParsingSchema


class VarArgsParsingSchemaTest(PythonicTestCase):
    
    class VarArgsSchema(VarArgsParsingSchema):
        parameter_order = ('id', 'items')
        id = IntegerValidator()
        items = Validator()
    
    def schema_class(self):
        return self.__class__.VarArgsSchema
    
    def schema(self):
        return self.schema_class()()
    
    # ---- tests ---------------------------------------------------------------
    
    def test_validates_string_with_one_item(self):
        self.assert_equals(dict(id=1, items=['foo']), self.schema().process('1, foo'))
    
    def test_consumes_multiple_items_in_string(self):
        self.assert_equals(dict(id=1, items=['foo', 'bar']), 
                           self.schema().process('1, foo, bar'))
    

