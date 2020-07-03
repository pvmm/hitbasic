from .helper import *

from . import language_types as types


def UNARY_OP_TYPE(*type):
    return {
        ('Not', types.Integer): types.Integer,
        ('Not', types.Single): types.Integer,
        ('Not', types.Double): types.Integer,
        ('-', types.Single): types.Single,
        ('-', types.Double): types.Double,
        ('-', types.Integer): types.Integer,
    }[type]


# MSX-BASIC priority table
OP_PRIORITY = {
        '^': 13,
        'S': 12, # [S]ignal
        '*': 11, '//': 11,
        '\\': 10,
        'Mod': 9,
        '+': 8, '-': 8,
        '=': 7, '<>': 7, '<=': 7, '<': 7, '>=': 7, '>': 7, 'Is': 7, 'IsNot': 7,
        'Not': 6,
        'And': 5,
        'Or': 4,
        'Xor': 3,
        'Eqv': 2,
        'Imp': 1,
        ',': 0, ';': 0, 'A': 0 # [A]ttribution
}


class MSX1_Architecture(object):

    SCREEN_MODES = [0, 1, 2, 3]
    SPRITE_SIZE = [0, 1, 2, 3]
    KEY_CLICK = [0, 1]
    BAUD_RATE = [1, 2]
    PRINTER_TYPE = [0, 1]


    @property
    def INTERLACE_MODE():
        raise SyntaxError('interlace mode not available on the MSX1')


    @classmethod
    def screen_attrs(klass):
        return [klass.SCREEN_MODES, klass.SPRITE_SIZE, klass.KEY_CLICK, klass.BAUD_RATE, klass.PRINTER_TYPE]


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
