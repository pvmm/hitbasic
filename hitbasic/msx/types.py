from hitbasic.language_support import Function, Array, Scalar
from hitbasic.helpers.tuple import make_tuple


Integer = 0
String = 1
Single = 2
Double = 3
Any = 4
OptInteger = 5

default_type = Integer
current_default_type_name = 'Integer'

TYPEDES_CHARS = [ '$', '%', '#', '!' ]
TYPEDES2NAME_MAPPING = { '$' : 'String', '%' : 'Integer', '#' : 'Double', '!' : 'Single' }
NAME2TYPEDES_MAPPING = { 'String' : '$', 'Integer' : '%', 'Double' : '#', 'Single' : '!' }
NAME2NUM_MAPPING = { 'String' : String, 'Integer' : Integer, 'Double' : Double, 'Single' : Single }
NUM2TYPEDES_MAPPING = { String : '$', Integer : '%', Double : '#', Single : '!' }
TYPEDES2NUM_MAPPING = { '$' : String, '%' : Integer, '#' : Double, '!' : Single }


def get_basic_typedes_char(type_):
    assert type_ != None
    if type(type_) == str:
        return NAME2TYPEDES_MAPPING[type_]
    else:
        return NUM2TYPEDES_MAPPING[type_]


def strip_attrs_from_id(identifier):
    assert type(identifier) == str
    if identifier.endswith('()'):
        return identifier[:-3] if identifier[-3] in TYPEDES_CHARS else identifier[:-2]
    return identifier[:-1] if identifier[-1] in TYPEDES_CHARS else identifier


def get_type_from_id(identifier):
    assert type(identifier) == str
    if identifier.endswith('()'):
        if identifier[-3] in TYPEDES2NAME_MAPPING:
            return TYPEDES2NUM_MAPPING[identifier[-3]]

    if identifier[-1] in TYPEDES2NAME_MAPPING:
        return TYPEDES2NUM_MAPPING[identifier[-1]]

    return default_type


#
# Symbol table types
#


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
    'reference to HitBasic function in AST'
    def __init__(self, identifier, params=(), type=None):
        self.identifier = identifier
        self.params = make_tuple(params)
        self.type = type


    def check_params(self, params):
        'Match function call to function signature through regex' 
        param_map = { Integer: '(i|n)', OptInteger: '(i|n)?', Single: '(s|n)', Double: '(d|n)', String: 's', Any: '.', }
        func_map = { Integer: 'i', Single: 's', Double: 'd', String: 's'}
        pattern = functools.reduce(operator.add, [param_map[p.type] for p in self.params])
        funcall = functools.reduce(operator.add, [func_map[p.type] for p in params])
        if not re.match(pattern, funcall):
            raise TypeMismatch(printable(type), printable_type(value))


class BASICVar(Callee):
    'Reference to previously declared variable in AST'
    def __init__(self, identifier, reference=None, ranges=(), type_=None, init_value=None):
        self.identifier = identifier
        self.reference = reference
        self.ranges = make_tuple(ranges)
        self.init_value = init_value
        self.type = type_


    def __str__(self):
        return self.identifier


    def __repr__(self):
        return f'BASICVar({self.identifier})'


    def check_boundaries(self, params):
        if len(params) != len(self.ranges):
            raise ParameterCount(len(self.ranges), len(params))
        for (range, position) in zip(self.ranges, params):
            if position.value < range.begin or position.value > range.end:
                raise OutOfBounds(range)

