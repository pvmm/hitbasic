from . import ClauseComponents

from ..hitbasic import Surrogate
from ..exceptions import *
from ..helper import *


def __init__(self, rule, position, error, *points, **kwargs):
    dst_point = points[-1]
    src_point = points[0] if len(points) > 1 else ()
    Surrogate.__init__(self, rule, position, error, src_point=src_point, dst_point=dst_point, **kwargs)


def translate(self):
    if self.src_point:
        x, y, step = self.src_point
        src = ['STEP(' if step else '(', ' ', x, ',', ' ', y, ')']
    else:
        src = []
    x, y, step = self.dst_point
    dst = ['STEP(' if step else '(', ' ', x, ',', ' ', y, ')']
    return ClauseComponents.from_arg_list(*src, '-', *dst).translate()


def __repr__(self):
    if self.src_point:
        x, y, step = self.src_point
        src = ' Step(%s, %s)' % (x, y) if step else '(%s, %s)' % (x, y)
    else:
        src = ''
    x, y, step = self.dst_point
    dst = '-Step(%s, %s)' % (x, y) if step else '(%s, %s)' % (x, y)
    return 'BoxClause%s%s' % (src, dst)


def __eq__(self, other):
    return repr(self) == repr(other)

