from . import ClauseComponents, StatementComponents

from ..helper import *
from ..hitbasic import Surrogate


class Statement:

    def __init__(self, rule, position, error, clauses, **kwargs):
        Surrogate.__init__(self, rule, position, error, clauses=make_tuple(clauses), **kwargs)


    def __str__(self):
        return 'Dim()'


    def __repr__(self):
        return str(self)


    def translate(self):
        statement = StatementComponents()

        if self.clauses:
            clauses = ClauseComponents()
            for clause in self.clauses:
                output = clause.translate()
                if output:
                    clauses.add(' ', ',', *output)
            if clauses:
                statement.add('DIM', ' ', ClauseComponents(clauses[2:]))

        result = statement.translate()
        return result

