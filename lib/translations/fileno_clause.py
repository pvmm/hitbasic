from . import ClauseComponents
from ..hitbasic import Surrogate
from .. import language_types as types


class Clause:

    def __init__(self, rule, position, error, fileno=None, **kwargs):
        if not fileno or not isinstance(fileno, types.Integer):
            raise SyntaxError()
        Surrogate.__init__(self, rule, position, error, fileno=fileno, **kwargs)


    def translate(self):
        return ClauseComponents.from_arg_list('#', self.fileno.value, ',')

