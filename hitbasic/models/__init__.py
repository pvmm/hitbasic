import os, pkgutil

modules = __all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
modules = list(__all__)

__all__ += [ 'modules' ]


class ASCIINode(object):
    multiline = False
    compound = False
    dirty = True
    label_type = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.init()

    def init(self):
        pass

    def fits(self, available):
        return len(str(self)) < available

    def __bytes__(self):
        return self.keyword.upper()

    def write(self, file):
        pass


Node = ASCIINode
