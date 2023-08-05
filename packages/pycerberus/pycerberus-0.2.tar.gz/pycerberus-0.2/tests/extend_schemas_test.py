# -*- coding: UTF-8 -*-

from pycerberus.api import Validator
from pycerberus.lib import PythonicTestCase
from pycerberus.schema import SchemaValidator
from pycerberus.validators import StringValidator


class ExtendSchemaTest(PythonicTestCase):
    
    class BasicSchema(SchemaValidator):
        id = Validator()
        formvalidators = (Validator(), )
    
    def schema_class(self):
        return self.__class__.BasicSchema
    
    def schema(self):
        return self.schema_class()()
    
    def known_fields(self, schema):
        return set(schema.fieldvalidators().keys())
    
    # test functions
    
    def test_can_add_additional_validators_to_existing_schema(self):
        schema = self.schema()
        extended_schema = SchemaValidator()
        extended_schema.add('name', StringValidator())
        extended_schema.add_missing_validators(schema)
        
        self.assert_equals(set(['id', 'name']), self.known_fields(extended_schema))
        self.assert_length(1, schema.formvalidators())
    
    def test_existing_keys_are_kept(self):
        schema = self.schema()
        extended_schema = SchemaValidator()
        extended_schema.add('id', StringValidator())
        extended_schema.add_missing_validators(schema)
        
        self.assert_equals(set(['id']), self.known_fields(schema))
        self.assert_isinstance(extended_schema.validator_for('id'), StringValidator)
    
    def test_adding_validators_appends_formvalidators(self):
        schema = self.schema()
        extended_schema = SchemaValidator()
        extended_schema.add('id', StringValidator())
        extended_schema.add_formvalidator(StringValidator())
        extended_schema.add_missing_validators(schema)
        
        self.assert_length(2, extended_schema.formvalidators())
    
    def test_can_add_validators_from_schema_in_a_declarative_way(self):
        class ExtendedSchema(self.schema_class()):
            name = StringValidator()
            formvalidators = (StringValidator(), )
        
        extended_schema = ExtendedSchema()
        self.assert_equals(set(['id', 'name']), self.known_fields(extended_schema))
        self.assert_length(2, extended_schema.formvalidators())
        self.assert_isinstance(extended_schema.formvalidators()[1], StringValidator)
    
    def test_existing_names_from_superclass_are_replaced(self):
        class ExtendedSchema(self.schema_class()):
            id = StringValidator()
        
        extended_schema = ExtendedSchema()
        self.assert_isinstance(extended_schema.validator_for('id'), StringValidator)


