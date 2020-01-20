from . import *
from ..hitbasic import Surrogate
from ..exceptions import *
from ..helper import *


def __init__(self, rule, position, error, var, **kwargs):
    if var.ranges and var.init_value:
        if var.init_value.dimensions is None:
            raise ScalarInitError(var.identifier)
    Surrogate.__init__(self, rule, position, error, var=var, **kwargs)


def translate(self):
    result = ClauseComponents()
    if self.var.ranges:
        ranges = interleave(self.var.ranges, (',', ' '))
        return result.add(self.var.short(), '(', *ranges, ')')
    return result

