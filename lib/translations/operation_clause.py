from . import ClauseComponents
from .. import language_types as types
from .. import msx

from ..hitbasic import Surrogate


class Clause:

    def __init__(self, rule, position, error, op, op1, op2, need_lparens=False, need_rparens=False, **kwargs):
        tmp = types.compare_types(op1.type, op2.type)
        type_ = types.Integer if msx.is_logic_op(op) else tmp
        Surrogate.__init__(self, rule, position, error, op=op, op1=op1, op2=op2, need_lparens=need_lparens, need_rparens=need_rparens, type=type_, **kwargs)


    @property
    def is_constexp(self):
        return self.op1.is_constexp and self.op2.is_constexp


    def literal_value(self):
        return msx.solve(self)


    def translate(self):
        op1 = ('(', self.op1, ')') if self.need_lparens else (self.op1,)
        op2 = ('(', self.op2, ')') if self.need_rparens else (self.op2,)
        return ClauseComponents.from_arg_list(*op1, ' ', self.op, ' ', *op2).translate()

