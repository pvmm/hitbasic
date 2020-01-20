from ..hitbasic import Surrogate

from . import CodeComponents
from .. import language_statements as statements


def __init__(self, rule, position, error, code_block, **kwargs):
    Surrogate.__init__(self, rule, position, error, code_block=code_block, **kwargs)


def translate(self):
    return CodeComponents(self.code_block).translate()

