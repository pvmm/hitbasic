from . import ClauseComponents

from ..hitbasic import Surrogate
from ..exceptions import *
from ..helper import *


class Clause:

    def __init__(self, rule, position, error, begin, end, *args, **kwargs):
        allow_reverse = kwargs.pop('allow_reverse', False)
        allow_negative = kwargs.pop('allow_negative', False)
        allow_empty = kwargs.pop('allow_empty', False)

        if hasattr(begin, 'value'):
            begin = begin.value
        if hasattr(end, 'value'):
            end = end.value

        if begin != '*' and end != '*':
            if not allow_reverse and begin > end:
                raise ValueError('reverse range not allowed in this context')
            if not allow_negative and (begin < 0 or end < 0):
                raise TypeError('negative value in range not allowed in this context')

        Surrogate.__init__(self, rule, position, error, begin=begin, end=end, allow_empty=allow_empty, *args, **kwargs)


    def translate(self):
        if self.allow_empty and self.end == '*':
            return ClauseComponents()
        if self.end == '*':
            return ClauseComponents(10)
        if self.allow_empty and self.begin == '*':
            return ClauseComponents()
        if self.begin == '*':
            return ClauseComponents(0)
        return ClauseComponents(self.end - self.begin)


    def __str__(self):
        return 'RangeClause(%s, %s)' % (self.begin, self.end)


    def __eq__(self, other):
        return str(self) == str(other)

