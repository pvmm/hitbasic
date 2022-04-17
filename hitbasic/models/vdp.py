# VDP specific statements

import os

from hitbasic.helpers import string
from hitbasic.models import Node
from hitbasic import spacing, arg_spacing


class ScreenStmt(Node):
    keyword = 'SCREEN'

    def __str__(self):
        return f"%s{spacing}%s" % (self.keyword, string.write_list([self.mode, self.spriteSize,
                self.clickStatus, self.baudRate, self.printerType, self.interlaceMode]))


class ColorStmt(Node):
    keyword = 'COLOR'

    def __str__(self):
        return f"%s{spacing}%s" % (self.keyword, string.write_list([self.fg, self.bg, self.bd]))


class LineStmt(Node):
    keyword = 'LINE'

    def __str__(self):
        return f"%s{spacing}%s-%s%s" % (self.keyword, self.src if self.src else '', self.dst,
                self.args if self.args else '')


class PaintStmt(Node):
    keyword = 'PAINT'

    def __str__(self):
        return f"%s{spacing}%s%s" % (self.keyword, self.pt, self.args)


class PresetStmt(Node):
    keyword = 'PRESET'

    def __str__(self):
        return f"%s{spacing}%s%s" % (self.keyword, self.pt, self.args)


class PsetStmt(PresetStmt):
    keyword = 'PSET'


class StepPtArg(Node):
    def __str__(self):
        return f'%s(%s{arg_spacing},%s)' % ('STEP' if self.step else '', self.coor.x, self.coor.y)

