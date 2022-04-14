import os, pkgutil

modules = __all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
modules = list(__all__)
__all__ += [ 'modules' ]
