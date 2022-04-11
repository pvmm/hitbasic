from . import ClauseComponents
from ..hitbasic import Surrogate
from ..helper import *
from .. import language_types as types
from .. import language_statements as statements


class Clause:

    def __init__(self, rule, position, error, value, params, **kwargs):
        Surrogate.__init__(self, rule, position, error, value=value, params=make_tuple(params), **kwargs)


    @property
    def is_constexp(self):
        # TODO: detect if object is a constant and change this attribute to True
        return False


    @property
    def type(self):
        if not self.value:
            raise AttributeError('reference cannot be located')
        return self.value.type


    def literal_value(self):
        if not self.value:
            raise AttributeError('reference cannot be located')
        if isinstance(self.value, types.BASICVar):
            return self.value.init_value
        raise TypeError()


    def translate(self):
        clause = ClauseComponents()

        if not self.value:
            raise AttributeError('reference cannot be located')

        if isinstance(self.value, (types.BASICVar, types.BuiltIn)):
            if self.params:
                inner_clause = interleave(self.params, (',', ' '))
                clause.add(self.value.short(), '(', *inner_clause, ')')
            else:
                clause.append(self.value.short())

        result = clause.translate()
        return result
