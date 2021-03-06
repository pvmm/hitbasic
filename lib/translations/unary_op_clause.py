from . import ClauseComponents

from .. import msx
from .. import language_types as types

from ..hitbasic import Surrogate
from ..exceptions import *


class Clause:

    def __init__(self, rule, position, error, op, operand, need_parens=False, **kwargs):
        try:
            msx.unary_op_type(op, operand.type)
        except KeyError:
            raise TypeMismatch(types.printable(msx.get_op_type(op)), types.printable(operand.type), operand.value.reference)
        type_ = types.Integer if msx.is_logic_op(op) else operand.type
        Surrogate.__init__(self, rule, position, error, op=op, operand=operand, need_parens=need_parens, type=type_, **kwargs)


    def translate(self):
        operand = ('(', self.operand, ')') if self.need_parens else (self.operand,)
        return ClauseComponents.from_arg_list(self.op.upper(), ' ', *operand).translate()
