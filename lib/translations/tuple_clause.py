from . import ClauseComponents
from .. import language_clauses as clauses

from ..hitbasic import Surrogate
from ..exceptions import *
from ..helper import *


class Clause:

    def __init__(self, rule, position, error, values, use_parentheses=False, **kwargs):
        Surrogate.__init__(self, rule, position, error, values=values, use_parentheses=use_parentheses, **kwargs)


    def translate(self):
        previous, next = (['('], [')']) if self.use_parentheses else ([], [])
        values = interleave(self.values, delims=(',', ' '))
        return ClauseComponents.from_arg_list(*previous, *values, *next).translate()


    def __repr__(self):
        return 'Tuple'


    def __eq__(self, other):
        return repr(self) == repr(other)
