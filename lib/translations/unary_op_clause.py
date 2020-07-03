from . import ClauseComponents

from .. import msx
from .. import language_types as types

from ..hitbasic import Surrogate


class Clause:

    def __init__(self, rule, position, error, op, operand, need_parens=False, **kwargs):
        type_ = msx.UNARY_OP_TYPE(op, operand.type)
        Surrogate.__init__(self, rule, position, error, op=op, operand=operand, need_parens=need_parens, type=type_, **kwargs)


    def translate(self):
        operand = ('(', self.operand, ')') if self.need_parens else (self.operand,)
        return ClauseComponents.from_arg_list(self.op, ' ', *operand).translate()

