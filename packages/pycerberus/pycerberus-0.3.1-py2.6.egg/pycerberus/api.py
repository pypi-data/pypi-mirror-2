# -*- coding: UTF-8 -*-
#
# The MIT License
# 
# Copyright (c) 2009-2010 Felix Schwarz <felix.schwarz@oss.schwarz.eu>
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

import inspect

from pycerberus.compat import reversed, set
from pycerberus.errors import EmptyError, InvalidArgumentsError, InvalidDataError, \
    ThreadSafetyError
from pycerberus.i18n import _, GettextTranslation
from pycerberus.lib import SuperProxy

__all__ = ['BaseValidator', 'Validator']


class NoValueSet(object):
    pass


class EarlyBindForMethods(type):
    
    super = SuperProxy()
    
    def __new__(cls, classname, direct_superclasses, class_attributes_dict):
        validator_class = type.__new__(cls, classname, direct_superclasses, class_attributes_dict)
        cls._simulate_early_binding_for_message_methods(validator_class)
        return validator_class
    
    def _simulate_early_binding_for_message_methods(cls, validator_class):
        # Need to create a dynamic method if messages are defined in a 
        # class-level dict.
        if not callable(validator_class.messages):
            messages_dict = validator_class.messages.copy()
            def messages(self):
                return messages_dict
            validator_class.messages = messages
        
        # We need to simulate 'early binding' so that we can reference the 
        # messages() method which is defined in the class to be created!
        def keys(self):
            return validator_class.messages(self)
        # make sphinx happy
        keys.__doc__ = validator_class.keys.__doc__
        validator_class.keys = keys
        
        if validator_class.__name__ == 'BaseValidator' or \
            getattr(validator_class.message_for_key, 'autogenerated', False):
            def message_for_key(self, key, context):
                return validator_class.messages(self)[key]
            message_for_key.autogenerated = True
            # make sphinx happy
            message_for_key.__doc__ = validator_class.message_for_key.__doc__
            validator_class.message_for_key = message_for_key
    _simulate_early_binding_for_message_methods = classmethod(_simulate_early_binding_for_message_methods)


class BaseValidator(object):
    """The BaseValidator implements only the minimally required methods. 
    Therefore it does not put many constraints on you. Most users probably want 
    to use the ``Validator`` class which already implements some commonly used 
    features."""
    
    __metaclass__ = EarlyBindForMethods
    super = SuperProxy()
    
    def messages(self):
        """Return all messages which are defined by this validator as a 
        key/message dictionary. Alternatives you can create a class-level
        dictionary which contains these keys/messages.
        
        You must declare all your messages here so that all keys are known 
        after this method was called.
        
        Calling this method might be costly when you have a lot of messages and 
        returning them is expensive. You can reduce the overhead in some 
        situations by implementing ``message_for_key()``"""
        return {}
    
    def message_for_key(self, key, context):
        """Return a message for a specific key. Implement this method if you 
        want to avoid calls to messages() which might be costly."""
        raise NotImplementedError('message_for_key() should have been replaced by a metaclass')
    
    def keys(self):
        """Return all keys defined by this specific validator class."""
        raise NotImplementedError('keys() should have been replaced by a metaclass')
    
    def error(self, key, value, context, errorclass=InvalidDataError, **values):
        """Raise an InvalidDataError for the given key."""
        msg_template = self.message_for_key(key, context)
        raise errorclass(msg_template % values, value, key=key, context=context)
    
    def process(self, value, context=None):
        """This is the method to validate your input. The validator returns a
        (Python) representation of the given input ``value``.
        
        In case of errors a ``InvalidDataError`` is thrown."""
        return value
    
    def as_string(self, value, context=None):
        """Return the (Python) value as string which could be converted back to
        the given value using this validator. This is useful for widget 
        libraries like ToscaWidgets."""
        return str(value)


class Validator(BaseValidator):
    """The Validator is the base class of most validators and implements 
    some commonly used features like required values (raise exception if no
    value was provided) or default values in case no value is given.
    
    This validator splits conversion and validation into two separate steps:
    When a value is ``process()``ed, the validator first calls ``convert()`` 
    which performs some checks on the value and eventually returns the converted
    value. Only if the value was converted correctly, the ``validate()`` 
    function can do additional checks on the converted value and possibly raise 
    an Exception in case of errors. If you only want to do additional checks 
    (but no conversion) in your validator, you can implement ``validate()`` and
    simply assume that you get the correct Python type (e.g. int). 
    
    Of course if you can also raise a ``ValidationError`` inside of ``convert()`` -
    often errors can only be detected during the conversion process.
    
    By default, a validator will raise an ``InvalidDataError`` if no value was
    given (unless you set a default value). If ``required`` is False, the 
    default is None. All exceptions thrown by validators must be derived from 
    ``ValidationError``. Exceptions caused by invalid user input should use 
    ``InvalidDataError`` or one of the subclasses.
    
    If ``strip`` is True (default is False) and the input value has a ``strip()``
    method, the input will be stripped before it is tested for empty values and
    passed to the ``convert()``/``validate()`` methods.
    
    In order to prevent programmer errors, an exception will be raised if 
    you set ``required`` to True but provide a default value as well.
    """
    
    def __init__(self, default=NoValueSet, required=NoValueSet, strip=False):
        self.super()
        self._default = default
        self._required = required
        self._check_argument_consistency()
        self._strip_input = strip
        self._implementations, self._implementation_by_class = self._freeze_implementations_for_class()
        if self.is_internal_state_frozen() not in (True, False):
            self._is_internal_state_frozen = True
    
    # --------------------------------------------------------------------------
    # initialization
    
    def _check_argument_consistency(self):
        if self.is_required(set_explicitely=True) and self._has_default_value_set():
            msg = 'Set default value (%s) has no effect because a value is required.' % repr(self._default)
            raise InvalidArgumentsError(msg)
    
    def _has_default_value_set(self):
        return (self._default is not NoValueSet)
    
    def _freeze_implementations_for_class(self):
        class_for_key = {}
        implementations_for_class = {}
        known_functions = set()
        for cls in reversed(inspect.getmro(self.__class__)):
            if self._class_defines_custom_keys(cls, known_functions):
                known_functions.add(cls.keys)
                for key in cls.keys(self):
                    class_for_key[key] = self._implementations_by_key(cls)
                    implementations_for_class[cls] = class_for_key[key]
        return class_for_key, implementations_for_class
    
    def _implementations_by_key(self, cls):
        implementations_by_key = dict()
        for name in ['translation_parameters', 'keys', 'message_for_key', 'translate_message']:
            implementations_by_key[name] = getattr(cls, name)
        return implementations_by_key
    
    def _class_defines_custom_keys(self, cls, known_functions):
        return hasattr(cls, 'keys') and cls.keys not in known_functions
    
    # --------------------------------------------------------------------------
    # Implementation of BaseValidator API
    
    def messages(self):
        return {'empty': _('Value must not be empty.')}
    
    def error(self, key, value, context, errorclass=InvalidDataError, **values):
        translated_message = self.message(key, context, **values)
        raise errorclass(translated_message, value, key=key, context=context)
    
    def process(self, value, context=None):
        if context is None:
            context = {}
        if self._strip_input and hasattr(value, 'strip'):
            value = value.strip()
        value = super(Validator, self).process(value, context)
        if self.is_empty(value, context) == True:
            if self.is_required() == True:
                self.error('empty', value, context, errorclass=EmptyError)
            return self.empty_value(context)
        converted_value = self.convert(value, context)
        self.validate(converted_value, context)
        return converted_value
    
    # --------------------------------------------------------------------------
    # Defining a convenience API
    
    def convert(self, value, context):
        """Convert the input value to a suitable Python instance which is 
        returned. If the input is invalid, raise an ``InvalidDataError``."""
        return value
    
    def validate(self, converted_value, context):
        """Perform additional checks on the value which was processed 
        successfully before (otherwise this method is not called). Raise an 
        InvalidDataError if the input data is invalid.
        
        You can implement only this method in your validator if you just want to
        add additional restrictions without touching the actual conversion.
        
        This method must not modify the ``converted_value``."""
        pass
    
    def empty_value(self, context):
        """Return the 'empty' value for this validator (usually None)."""
        if self._default is NoValueSet:
            return None
        return self._default
    
    def is_empty(self, value, context):
        """Decide if the value is considered an empty value."""
        return (value is None)
    
    def is_required(self, set_explicitely=False):
        if self._required == True:
            return True
        elif (not set_explicitely) and (self._required == NoValueSet):
            return True
        return False
    
    # -------------------------------------------------------------------------
    # i18n: public API
    
    def translation_parameters(self, context):
        return {'domain': 'pycerberus'}
    
    def translate_message(self, key, native_message, translation_parameters, context):
        # This method can be overridden on a by-class basis to get translations 
        # to support non-gettext translation mechanisms (e.g. from a db)
        translated_message = GettextTranslation(**translation_parameters).gettext(native_message)
        # Somehow gettext in Python 2.6 does not translate the read strings 
        # from mo files even if this was declared in the po file...
        # Currently we just default to UTF-8 but this should be more flexible
        # somehow...
        # However in Python 2.3 gettext returns unicode instances already...
        if isinstance(translated_message, unicode):
            return translated_message
        return translated_message.decode('UTF-8')
    
    def message(self, key, context, **values):
        # This method can be overridden globally to use a different message 
        # lookup / translation mechanism altogether
        native_message = self._implementation(key, 'message_for_key', context)(key)
        translation_parameters = self._implementation(key, 'translation_parameters', context)()
        translation_function = self._implementation(key, 'translate_message', context)
        translated_template = translation_function(key, native_message, translation_parameters)
        return translated_template % values
    
    # -------------------------------------------------------------------------
    # private 
    
    def _implementation(self, key, methodname, context):
        def context_key_wrapper(*args):
            method = self._implementations[key][methodname]
            args = list(args) + [context]
            return method(self, *args)
        return context_key_wrapper
    
    def is_internal_state_frozen(self):
        is_frozen = getattr(self, '_is_internal_state_frozen', NoValueSet)
        if is_frozen == NoValueSet:
            return None
        return bool(is_frozen)
    
    def set_internal_state_freeze(self, is_frozen):
        self.__dict__['_is_internal_state_frozen'] = is_frozen
    
    def __setattr__(self, name, value):
        "Prevent non-threadsafe use of Validators by unexperienced developers"
        if self.is_internal_state_frozen():
            raise ThreadSafetyError('Do not store state in a validator instance as this violates thread safety.')
        self.__dict__[name] = value
    
    # -------------------------------------------------------------------------


