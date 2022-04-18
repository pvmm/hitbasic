import os, pkgutil

modules = __all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
modules = list(__all__)

__all__ += [ 'modules' ]


NO_LABEL = 0
NUMERIC = 1
PLACEHOLDER = 2


class Node(object):
    multiline = False
    compound = False
    dirty = True
    label_type = NO_LABEL

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def need_break(self, line_len):
        return len(str(self)) > line_len

    def __str__(self):
        return self.keyword.upper()

    def write(self, file):
        pass
