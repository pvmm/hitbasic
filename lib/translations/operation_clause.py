from . import ClauseComponents
from ..hitbasic import Surrogate
from .. import language_types as types


def __init__(self, rule, position, error, op, op1, op2, **kwargs):
    type_ = types.compare_types(op1.type, op2.type)
    Surrogate.__init__(self, rule, position, error, op=op, op1=op1, op2=op2, type=type_, **kwargs)


@property
def is_constexp(self):
    return self.op1.is_constexp and self.op2.is_constexp


def literal_value(self):
    return msxbasic.solve(self)


def translate(self):
    return ClauseComponents.from_arg_list(self.op1, ' ', self.op, ' ', self.op2).translate()

