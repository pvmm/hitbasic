from . import ClauseComponents

from .. import msx
from .. import language_types as types

from ..hitbasic import Surrogate


class Clause:

    def __init__(self, rule, position, error, op, operand, **kwargs):
        type_ = msx.UNARY_OP_TYPE(op, operand.type)
        Surrogate.__init__(self, rule, position, error, op=op, operand=operand, type=type_, **kwargs)


    def translate(self):
        return ClauseComponents.from_arg_list(self.op, ' ', self.operand).translate()

