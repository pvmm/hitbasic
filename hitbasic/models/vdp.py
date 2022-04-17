# VDP specific statements

import os

from hitbasic.helpers import string
from hitbasic.models import Node
from hitbasic import spacing, arg_spacing


class ScreenStmt(Node):
    keyword = 'SCREEN'

    def __str__(self):
        return f"%s{spacing}%s" % (self.keyword, string.write_list([self.mode, self.spriteSize, self.clickStatus,
            self.baudRate, self.printerType, self.interlaceMode]))


class ColorStmt(Node):
    keyword = 'COLOR'

    def __str__(self):
        return f"%s{spacing}%s" % (self.keyword, string.write_list([self.fg, self.bg, self.bd]))


class LineStmt(Node):
    keyword = 'LINE'

    def __str__(self):
        return f"%s{spacing}%s" % (self.keyword, string.write_list([self.pt]))


class PresetStmt(Node):
    keyword = 'PRESET'


class PsetStmt(Node):
    keyword = 'PSET'


class PtArg(Node):
    def __str__(self):
        return f'(%i{arg_spacing},%i)' % (self.x, self.y)
