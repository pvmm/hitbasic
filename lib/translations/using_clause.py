from . import ClauseComponents
from ..hitbasic import Surrogate
from ..helper import *


class Clause:

    def __init__(self, rule, position, error, format=None, params=None, **kwargs):
        if not format or not params:
            raise SyntaxError()
        Surrogate.__init__(self, rule, position, error, format=format, params=make_tuple(params), **kwargs)


    def translate(self):
        clause = ClauseComponents.from_arg_list('Using', ' ', self.format, ';')
        clause.append(insert(ClauseComponents(self.params), ' ', after=(',', ';')))
        return clause.translate()

