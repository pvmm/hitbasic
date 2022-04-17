# VDP specific statements

import os

from hitbasic.helpers import string
from hitbasic.models import Node
from hitbasic import spacing


class ScreenStmt(Node):
    def __str__(self):
        return f"SCREEN{spacing}%s%s" % (self.mode, string.write_list([self.spriteSize, self.clickStatus,
            self.baudRate, self.printerType, self.interlaceMode]))


class ColorStmt(Node):
    pass


class LineStmt(Node):
    pass


class PresetStmt(Node):
    pass


class PsetStmt(Node):
    pass
