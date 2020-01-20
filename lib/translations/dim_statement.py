from . import ClauseComponents, StatementComponents

from ..helper import *
from ..hitbasic import Surrogate


def __init__(self, rule, position, error, clauses, **kwargs):
    Surrogate.__init__(self, rule, position, error, clauses=make_tuple(clauses), **kwargs)


def translate(self):
    statement = StatementComponents()

    if self.clauses:
        clauses = []
        for clause in self.clauses:
            output = clause.translate()
            if output:
                clauses.extend([' ', ',', *output])
        if clauses:
            statement.add('DIM', ' ', ClauseComponents(clauses[2:]))

    return statement.translate()

