from . import ClauseComponents
from .. import language_clauses as clauses

from ..hitbasic import Surrogate
from ..exceptions import *
from ..helper import *


class Clause:

    def __init__(self, rule, position, error, case_type=clauses.CASE_IS, params=(), **kwargs):
        Surrogate.__init__(self, rule, position, error, case_type=case_type, params=params, **kwargs)


    def translate(self):
        return ClauseComponents()


    def __repr__(self):
        return 'Case(%s)' % ('Else' if self.case_type == clauses.CASE_ELSE else 'Is')


    def __eq__(self, other):
        return repr(self) == repr(other)

