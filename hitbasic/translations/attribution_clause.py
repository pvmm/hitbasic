from . import ClauseComponents

from ..hitbasic import Surrogate
from ..exceptions import *
from ..helper import *


class Clause:

    def __init__(self, rule, position, error, lvalue, rvalue, **kwargs):
        Surrogate.__init__(self, rule, position, error, lvalue=lvalue, rvalue=rvalue, **kwargs)


    def translate(self):
        return ClauseComponents.from_arg_list(self.lvalue, ' ', '=', ' ', self.rvalue).translate()


    def __repr__(self):
        return 'Attribution(%s = %s)' % (str(self.lvalue), str(self.rvalue))


    def __eq__(self, other):
        return repr(self) == repr(other)
