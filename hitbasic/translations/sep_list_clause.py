from . import ClauseComponents
from .. import language_clauses as clauses
from .. import language_types as types

from ..hitbasic import Surrogate
from ..exceptions import *
from ..helper import *


class Clause:

    def __init__(self, rule, position, error, *args, sep=',', list_type=clauses.REGULAR, **kwargs):
        Surrogate.__init__(self, rule, position, error, args=args, sep=sep, list_type=list_type, **kwargs)


    def translate(self):
        result = ClauseComponents()
        if self.args:
            if self.list_type == clauses.REGULAR:
                args = [s.upper() if type(s) == str else s.translate() for s in self.args]
            else:
                args = [('@%s' % s) if type(s) == str else s.translate() for s in self.args]
            args = interleave(args, delims=(self.sep, ' '))
            result.add(*args)
        return result.translate()


    def __repr__(self):
        return 'Args(%s)' % self.sep


    def __eq__(self, other):
        return repr(self) == repr(other)
