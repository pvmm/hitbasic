from . import ClauseComponents, StatementComponents
from .. import language_statements as statements

from ..hitbasic import Surrogate
from ..helper import *


debug = lambda *x: 0


class Statement:

    def __init__(self, rule, position, error, tokens=(), params=(), sep=(',', ' '), **kwargs):
        if not tokens: raise SyntaxError('unknown statement, tokens not specified')
        Surrogate.__init__(self, rule, position, error, tokens=make_tuple(tokens), params=make_tuple(params),
                sep=make_tuple(sep), **kwargs)


    def __str__(self):
        return '%s(%s)' % (''.join([token.title() for token in self.tokens]), '*')


    def __repr__(self):
        return str(self)


    def __eq__(self, other):
        if isinstance(other, str):
            return ' '.join(self.tokens).upper() == other.upper()
        if isinstance(other, statements.Statement):
            return self.tokens == other.tokens
        return False


    def translate(self):
        debug('self.params =', self.params)
        statement = StatementComponents(' '.join([token.upper() for token in self.tokens]))
        debug('statement =', statement)
        params = ClauseComponents(self.params)
        debug('params =', params)
        if self.sep: params = interleave(params, self.sep)
        debug('interleave result =', params)
        if len(statement) > 0 and params: statement.add(' ', *params)
        debug('statement =', statement)
        return statement.translate()
