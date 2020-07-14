from contextlib import suppress

from . import ClauseComponents
from ..hitbasic import Surrogate


class Type:

    def __init__(self, rule, position, error, value, type, *args, **kwargs):
        Surrogate.__init__(self, rule, position, error, value=value, type=type, is_constexp=True, **kwargs)


    def new(self, klass, value, type=None, **kwargs):
        return klass(self.rule, self.position, self.error, value=value, type=type or self.type, **kwargs)


    def literal_value(self):
        return self.value


    def translate(self):
        return str(self.value)


    def __lt__(self, other):
        with suppress(AttributeError):
            return self.value < other.value
        return self.value < other


    def __gt__(self, other):
        with suppress(KeyError):
            return self.value > other.value
        return self.value > other


    def __eq__(self, other):
        with suppress(AttributeError):
            return self.value == other.value
        return self.value == other


    def __add__(self, other):
        with suppress(AttributeError):
            return self.new(self.__class__, self.literal_value() + other.literal_value(), position_end=other.position)
        return self.new(self.__class__, self.literal_value() + other, position_end=self.position)


    def __sub__(self, other):
        with suppress(AttributeError):
            return self.new(self.__class__, self.literal_value() - other.literal_value(), position_end=other.position)
        return self.new(self.__class__, self.literal_value() - other, position_end=self.position)


    def __mod__(self, other):
        with suppress(AttributeError):
            return Integer(self.literal_value() % other.literal_value(), position=self.position, position_end=other.position)
        return Integer(self.literal_value() % other, position=self.position, position_end=self.position)


    def __mul__(self, other):
        with suppress(AttributeError):
            return self.new(self.__class__, self.literal_value() * other.literal_value(), position_end=other.position)
        return self.new(self.__class__, self.literal_value() * other, position_end=self.position)


    def __truediv__(self, other):
        with suppress(AttributeError):
            return Double(self.literal_value() / other.literal_value(), position=self.position, position_end=other.position)
        return Double(self.literal_value() / other, position=self.position, position_end=self.position)


    def __floordiv__(self, other):
        with suppress(AttributeError):
            return Integer(int(self.literal_value() / other.literal_value()), position=self.position, position_end=other.position)
        return Integer(int(self.literal_value() / other), position=self.position, position_end=self.position)


    def __pow__(self, other):
        with suppress(AttributeError):
            return self.new(self.__class__, self.literal_value() ** other.literal_value(), position_end=other.position)
        return self.new(self.__class__, self.literal_value() ** other, position_end=self.position)
