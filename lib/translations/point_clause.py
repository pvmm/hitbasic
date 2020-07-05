from . import ClauseComponents

from ..hitbasic import Surrogate
from ..exceptions import *
from ..helper import *


class Clause:

    def __init__(self, rule, position, error, x, y, step, **kwargs):
        Surrogate.__init__(self, rule, position, error, x=x, y=y, step=step, **kwargs)


    def translate(self):
        return ClauseComponents.from_arg_list('STEP(' if self.step else '(', self.x, ',', ' ', self.y, ')').translate()


    def __repr__(self):
        return 'PointClause(%s)' % ('Step(%s, %s)' % (self.x, self.y) if self.step else '%s, %s' % (self.x, self.y))


    def __eq__(self, other):
        return str(self) == str(other)
