from . import ClauseComponents, StatementComponents
from .. import language_statements as statements

from ..hitbasic import Surrogate
from ..helper import *


debug = lambda *x: 0


class Statement:

    def __init__(self, rule, position, error, tokens=(), params=(), sep=(',', ' '), **kwargs):
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
        debug('Begin %s' % self)
        debug('self.params =', self.params)
        instruction = ' '.join([token.upper() for token in self.tokens])
        debug('instruction =', instruction)
        if instruction: statement = StatementComponents(instruction)
        else: statement = StatementComponents()
        params = ClauseComponents(self.params)
        debug('params =', params)
        if self.sep: params = interleave(params, self.sep)
        debug('interleave result =', params)
        if instruction and params: statement.add(' ', *params)
        elif params: statement.add(*params)
        debug('statement =', statement)
        debug('End %s' % self)
        return statement.translate()
