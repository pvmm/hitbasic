from ..hitbasic import Surrogate

from . import token
from . import ClauseComponents
from .. import language_types as types


class Clause:

    def __init__(self, rule, position, error, op, op2, need_rparens=False, **kwargs):
        Surrogate.__init__(self, rule, position, error, op=op, op2=op2, need_rparens=need_rparens, type=op2.type, **kwargs)


    @property
    def is_constexp(self):
        return False


    def literal_value(self):
        raise NotImplemented()


    def translate(self):
        op2 = ('(', self.op2, ')') if self.need_rparens else (self.op2,)
        return ClauseComponents.from_arg_list(self.op.upper(), ' ', *op2).translate()

