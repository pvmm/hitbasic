from . import ClauseComponents
from ..hitbasic import Surrogate


def __init__(self, rule, error, position, value, **kwargs):
    Surrogate.__init__(self, rule, error, position, value=value, type=value.type, **kwargs)


@property
def is_constexp(self):
    return self.value.is_constexp


def literal_value(self):
    if isinstance(self.value, (int, float, str, bool)):
        return self.value
    else:
        return self.value.literal_value()


def translate(self):
    return ClauseComponents(self.value)

