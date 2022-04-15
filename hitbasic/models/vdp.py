# VDP specific statements

import os

from ..helpers import string


class ScreenStmt(object):
    def __init__(self, parent, mode, spriteSize, clickStatus, baudRate, printerType, interlaceMode):
        self.spacing = os.getenv('HITBASIC_SPACING', ' ');
        self.parent = parent
        self.mode = mode
        self.spriteSize = spriteSize or ''
        self.clickStatus = clickStatus or ''
        self.baudRate = baudRate or ''
        self.printerType = printerType or ''
        self.interlaceMode = interlaceMode or ''

    def __str__(self):
        return f"SCREEN{self.spacing}%s%s" % (self.mode, string.writeList([self.spriteSize, self.clickStatus,
            self.baudRate, self.printerType, self.interlaceMode]))

    def write(self, file):
        pass
