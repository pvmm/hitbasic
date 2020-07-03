from .helper import *

from . import language_types as types


def UNARY_OP_TYPE(*type):
    return {
        ('Not', types.Integer): types.Integer,
        ('-', types.Single): types.Single,
        ('-', types.Double): types.Double,
        ('-', types.Integer): types.Integer,
    }[type]


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

