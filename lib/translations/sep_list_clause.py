from . import ClauseComponents

from ..hitbasic import Surrogate
from ..exceptions import *
from ..helper import *


def __init__(self, rule, position, error, sep=',', *args, **kwargs):
    Surrogate.__init__(self, rule, position, error, sep=sep, args=args, **kwargs)


def translate(self):
    if self.args:
        lst = interleave(self.args, delims=(self.sep, ' '))
        lst = [s.upper() if type(s) == str else s for s in lst]
        return ClauseComponents(lst).translate()
    return ClauseComponents()


def __repr__(self):
    return 'Args(%s)' % self.sep


def __eq__(self, other):
    return repr(self) == repr(other)

