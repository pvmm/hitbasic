import re
import operator
import functools

from . import NO_RULE
from . import msx

from .helper import *
from .exceptions import *
from .hitbasic import Surrogate


# fake types
Nil = type('Nil', (Surrogate,), { 'translate': lambda self: [] })
Any = type('Any', (Surrogate,), {}) # just for parameter matching in function calling
OptInteger = type('OptInteger', (Surrogate,), {})
Boolean = None

# MSX-BASIC types
String = None
Integer = None
Double = None
Single = None
DEFAULT_TYPE = Double

TYPES = { 'Nil': Nil, 'String' : None, 'Integer' : None, 'Double' : None, 'Single' : None, 'Boolean' : None,
          'Any': None }
ALLOWED_TYPE_NAMES = [ 'Nil', 'String', 'Integer', 'Double', 'Single', 'Address' ]
TYPE_CHARS = [ '$', '%', '#', '!' ]
NAME_MAPPING = { '$' : 'String', '%' : 'Integer', '#' : 'Double', '!' : 'Single' }
CHAR_MAPPING = { 'String' : '$', 'Integer' : '%', 'Double' : '#', 'Single' : '!' }
NUMBER_CLASS = { 'Boolean': 0, 'Integer': 1, 'Single': 2, 'Double': 3 }

READ_ONLY = 0
WRITE_ONLY = 1 # Not tecnically a function or variable


def numeric_classes():
    return (Integer, Double, Single)


def create_nil(**kwargs):
    position = kwargs.pop('pos', 0)
    return Nil(NO_RULE, position, False, **kwargs)


def printable_type(item):
    assert item != None
    return printable(type(item))


def printable(type_):
    assert type_ != None
    if hasattr(type_, '__name__') and type_.__name__:
        return type_.__name__
    else:
        return str(type)


def register(type_name, type_):
    'register language types "globally"'
    assert type(type_name) == str and type_ != None
    type_name = type_name.title()
    if type_name in ['String', 'Integer', 'Double', 'Single']:
        globals()[type_name] = type_
        globals()['TYPES'][type_name] = type_
    if type_name == 'Double':
        globals()['DEFAULT_TYPE'] = type_
        globals()['current_default_type'] = type_


def compare_types(type1, type2, coercion=True):
    assert type1 != None and type2 != None
    if (type1, type2) == (None, None):
        raise TypeMismatch()
    elif type1 is Any: return type2
    elif type2 is Any: return type1
    if type1 == type2:
        return type1
    if not coercion and type1 != type2:
        raise TypeMismatch(type1, type2)
    if printable(type1) in NUMBER_CLASS.keys() and printable(type2) == 'String':
        raise TypeMismatch(type1, type2)
    if printable(type2) in NUMBER_CLASS.keys() and printable(type1) == 'String':
        raise TypeMismatch(type1, type2)
    if NUMBER_CLASS[printable(type1)] > NUMBER_CLASS[printable(type2)]:
        return type1
    else:
        return type2


def compatible_types(type1, type2, coercion=True):
    'Treat None as a wildcard'
    assert type1 != None and type2 != None
    if None in (type1, type2):
        return True
    if type1 == type2:
        return True
    if not coercion and type1 != type2:
        return False
    if printable(type1) in NUMBER_CLASS.keys() and printable(type2) == 'String':
        return False
    if printable(type2) in NUMBER_CLASS.keys() and printable(type1) == 'String':
        return False
    return True


def check_initialisation(type_, value):
    'Return True if type check successes, otherwise return the incompatible type and value.'
    assert type_ != None and value != None
    if isinstance(value, list):
        for item in value:
            if isinstance(item, list):
                check_initialisation(type_, item)
            elif not compatible_types(type_.__name__, item.type.__name__):
                raise TypeMismatch(type_, item, search_position(item, value))
        return True
    if not compatible_types(printable(type_), printable_type(value)):
        raise TypeMismatch(type_, value.type, search_position(value))
    return True


def check_type(type_, value, coercion=False):
    assert type != None and value != None
    if not coercion:
        if isinstance(value, type_):
            return True
        else:
            return value
    else:
        if value.type in type_.base_type:
            return True
        else:
            return value


def get_type_from_id(identifier):
    assert type(identifier) == str
    if identifier.endswith('()'):
        if identifier[-3] in NAME_MAPPING:
            type_name = NAME_MAPPING[identifier[-3]]
            return globals()[type_name]

    if identifier[-1] in NAME_MAPPING:
        type_name = NAME_MAPPING[identifier[-1]]
        return globals()[type_name]

    return DEFAULT_TYPE


def get_basic_type_char(type_):
    assert type_ != None
    return CHAR_MAPPING[type_.__name__]


def get_type_from_type_id(type_id):
    assert type_id != None
    if (result := TYPES[type_id]) is None:
        raise ValueError('type not initialised')
    return result


def strip_attrs_from_id(identifier):
    assert type(identifier) == str
    if identifier.endswith('()'):
        return identifier[:-3] if identifier[-3] in TYPE_CHARS else identifier[:-2]
    return identifier[:-1] if identifier[-1] in TYPE_CHARS else identifier


class Callee:
    'because BASIC treats functions and arrays similarly'
    def shorter(self):
        if self.identifier.endswith('()'):
            if self.identifier[-3] in ['$', '%', '#', '!']:
                return self.identifier[:-3]
            return self.identifier[:-2]
        if self.identifier[-1] in ['$', '%', '#', '!']:
            return self.identifier[:-1]


    def short(self):
        if self.identifier.endswith('()'):
            return self.identifier[0:-2]
        return self.identifier


class Function(Callee):
    'reference to HitBasic function'
    def __init__(self, identifier, params=(), type=None):
        self.identifier = identifier
        self.params = make_tuple(params)
        self.type = type


    def check_params(self, params):
        pmap = { Integer: '(i|n)', OptInteger: '(i|n)?', Single: '(s|n)', Double: '(d|n)', String: 's', Any: '.', }
        fmap = { Integer: 'i', Single: 's', Double: 'd', String: 's'}
        pattern = functools.reduce(operator.add, [pmap[p.type] for p in self.params])
        funcall = functools.reduce(operator.add, [fmap[p.type] for p in params])
        if not re.match(pattern, funcall):
            raise TypeMismatch(type, value.type)


class BuiltIn(Callee):
    'reference to built-in BASIC function'
    def __init__(self, identifier, params=(), type=None, attrs=(), ver=msx.DEFAULT_BASIC_VER):
        self.identifier = identifier
        self.params = make_tuple(params)
        self.type = type
        self.attrs = make_tuple(attrs)
        self.ver = ver


    def __repr__(self):
        return 'BuiltIn(%s)' % self.identifier


class BASICVar(Callee):
    'reference to previously declared variable in symbol table'
    def __init__(self, identifier, reference=None, ranges=(), type=None, init_value=None):
        self.identifier = identifier
        self.reference = reference
        self.ranges = make_tuple(ranges)
        self.init_value = init_value
        self.type = type


    def __repr__(self):
        return 'BASICVar(%s)' % self.identifier


    def check_boundaries(self, params):
        if len(params) != len(self.ranges):
            raise ParameterCount(len(self.ranges), len(params))
        for (range, position) in zip(self.ranges, params):
            if position.value < range.begin or position.value > range.end:
                raise OutOfBounds(range)
