from types import SimpleNamespace

from .helper import *

from . import language_types as types


# BASIC version
VERSION_STR = ['MSX-BASIC ver1.0', 'MSX-BASIC ver2.0', 'DISK-BASIC ver1.0', 'DISK-BASIC ver2.0']
MSX_BASIC_1_0 = 0
MSX_BASIC_2_0 = 1
MSX_BASIC = MSX_BASIC_1_0
DISK_BASIC_1 = 2
DISK_BASIC_2 = 3
DISK_BASIC = DISK_BASIC_1
DEFAULT_BASIC_VER = MSX_BASIC


def get_op_type(op):
    if is_logic_op(op): return types.Boolean
    if is_arithmetic_op(op): return types.Double
    if is_string_op(op): return types.String


def unary_op_type(*type):
    return {
        ('Not', types.Integer): types.Integer,
        ('Not', types.Single): types.Integer,
        ('Not', types.Double): types.Integer,
        ('-', types.Single): types.Single,
        ('-', types.Double): types.Double,
        ('-', types.Integer): types.Integer,
    }[type]


def is_logic_op(op):
    return op.title() in ['Not', 'And', 'Or', 'Xor', 'Eqv', 'Imp', '=', '>=', '<=', '>', '<', '<>']


def is_arithmetic_op(op):
    return op.title() in ['^', '-', '*', '\\', 'Mod', '+', '']


# MSX-BASIC priority table
OP_PRIORITY = {
        '^': 13,
        'S': 12, # [S]ignal
        '*': 11, '//': 11,
        '\\': 10,
        'Mod': 9,
        '+': 8, '-': 8,
        '=': 7, '<>': 7, '<=': 7, '<': 7, '>=': 7, '>': 7, #'Is': 7, 'IsNot': 7,
        'Not': 6,
        'And': 5,
        'Or': 4,
        'Xor': 3,
        'Eqv': 2,
        'Imp': 1,
        #',': 0, ';': 0, 'A': 0 # [A]ttribution
}


class Instruction(SimpleNamespace): pass


class MSX1_Architecture(object):

    SCREEN_MODES = [0, 1, 2, 3]
    SPRITE_SIZE = [0, 1, 2, 3]
    KEY_CLICK = [0, 1]
    BAUD_RATE = [1, 2]
    PRINTER_TYPE = [0, 1]

    _stmt_lib = {
        # PLAY #<Device>,"<MmlStringChannel1>","<MmlStringChannel2>",...,"<MmlStringChannel13>"
        'PLAY' : Instruction(pattern='i?ss?s?s?s?s?s?s?s?s?s?s?s?', # max=13 channels
                             names=['Channel %s' % num for num in range(1, 13)]),
        # LINE [STEP(<X1>,<Y1>)]-STEP(<X2>,<Y2>),<Color>,<Shape>,<Operator>
        'LINE' : Instruction(pattern='p?pi?t?t?', names=['Point', 'Colour', 'Shape', 'Operator']),
        'PAINT': Instruction(pattern='pi?i?', names=['Point', 'Colour', 'Border Colour']),
        'PSET' : Instruction(pattern='pi?t?', names=['Point', 'Colour', 'Operator']),
    }


    @property
    def INTERLACE_MODE():
        raise SyntaxError_('interlace mode not available on the MSX1')


    @classmethod
    def screen_attrs(klass):
        return [klass.SCREEN_MODES, klass.SPRITE_SIZE, klass.KEY_CLICK, klass.BAUD_RATE, klass.PRINTER_TYPE]


    @classmethod
    def stmt_lib(klass, stmt_name):
        return klass._stmt_lib[stmt_name]


class MSX2_Architecture(MSX1_Architecture):

    # Replace MSX1 attributes
    SCREEN_MODES = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    INTERLACE_MODE = [0, 1, 2, 3]


    @classmethod
    def screen_attrs(klass):
        return [klass.SCREEN_MODES, klass.SPRITE_SIZE, klass.KEY_CLICK, klass.BAUD_RATE, klass.PRINTER_TYPE, klass.INTERLACE_MODE]


class MSX2P_Architecture(MSX2_Architecture):

    # Replace MSX2 attributes
    SCREEN_MODES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]


arch = {
        'msx2+': MSX2P_Architecture,
        'msx2': MSX2_Architecture,
        'msx1': MSX1_Architecture,
}
