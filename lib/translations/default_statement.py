from . import ClauseComponents, StatementComponents
from .. import language_statements as statements

from ..hitbasic import Surrogate
from ..helper import *


class Statement:

    def __init__(self, rule, position, error, tokens=(), params=(), arg_sep=(',', ' '), **kwargs):
        if not tokens: raise SyntaxError('unknown statement, tokens not specified')
        Surrogate.__init__(self, rule, position, error, tokens=make_tuple(tokens), params=make_tuple(params),
                arg_sep=make_tuple(arg_sep), **kwargs)


    def __eq__(self, other):
        if isinstance(other, statements.Statement):
            return self.tokens == other.tokens
        return False


    def translate(self):
        print('self.params =', self.params)
        statement = StatementComponents(' '.join([token.upper() for token in self.tokens]))
        debug('statement =', statement)
        debug('statement =', statement)
        params = ClauseComponents(self.params)
        print('params =', params)
        if self.arg_sep: params = interleave(params, self.arg_sep)
        print('interleave result =', params)
        if params: statement.add(' ', *params)
        debug('statement =', statement)
        return statement.translate()

