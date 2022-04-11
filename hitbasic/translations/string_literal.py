from . import ClauseComponents
from ..hitbasic import Surrogate


class Type:

    def __init__(self, rule, position, error, value, type, *args, **kwargs):
        Surrogate.__init__(self, rule, position, error, value=value, type=type, is_constexp=True, **kwargs)


    def literal_value(self):
        return self.value


    def translate(self):
        return '"%s"' % self.value


    def __str__(self):
        return self.value


    def __add__(self, other):
        with suppress(AttributeError):
            return self.__class__(self.value + other.value, position=self.position, position_end=self.position_end)
        return self.__class__(self.value + other, position=self.position, position_end=self.position_end)
