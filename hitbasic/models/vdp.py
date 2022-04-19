# VDP specific statements

import os

from hitbasic.helpers import string
from hitbasic.models import Node
from hitbasic import cfg


class ScreenStmt(Node):
    keyword = 'SCREEN'

    def __bytes__(self):
        return bytes(f"%s{cfg.spacing}%s" % (self.keyword, string.write_list([self.mode, self.spriteSize,
                self.clickStatus, self.baudRate, self.printerType, self.interlaceMode])), 'utf-8')


class ColorStmt(Node):
    keyword = 'COLOR'

    def __bytes__(self):
        return bytes(f"%s{cfg.spacing}%s" % (self.keyword, string.write_list([self.fg, self.bg, self.bd])), 'utf-8')


class LineStmt(Node):
    keyword = 'LINE'

    def __bytes__(self):
        return bytes(f"%s{cfg.spacing}%s-%s%s" % (self.keyword, self.src if self.src else '', self.dst,
                self.args if self.args else ''), 'utf-8')


class PaintStmt(Node):
    keyword = 'PAINT'

    def __bytes__(self):
        return bytes(f"%s{cfg.spacing}%s%s" % (self.keyword, self.pt, self.args), 'utf-8')


class PresetStmt(Node):
    keyword = 'PRESET'

    def __bytes__(self):
        return bytes(f"%s{cfg.spacing}%s%s" % (self.keyword, self.pt, self.args), 'utf-8')


class PsetStmt(PresetStmt):
    keyword = 'PSET'


class StepPtArg(Node):
    def __bytes__(self):
        return bytes(f'%s(%s{cfg.arg_spacing},%s)' % ('STEP' if self.step else '', self.coor.x, self.coor.y), 'utf-8')

