import inspect
import os, pkgutil
import textx

from hitbasic import msx
from hitbasic.exceptions import LineTooShort


__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
modules = list(__all__)

__all__ += [ 'modules' ]


def create_processors(symbol_table):
    processors = {}

    for module_name in modules:
        module = globals()[module_name]

        for key, value in module.__dict__.items():
            if not inspect.isclass(value):
                continue

            # class-specific processor method
            if hasattr(value, 'processor'):
                processors.update({ key : lambda stmt: stmt.processor(symbol_table) })

            # module-encompasing processor function
            elif inspect.isclass(value) and hasattr(module, 'processor'):
                processor = getattr(module, 'processor')
                processors.update({ key : lambda stmt: processor(stmt, symbol_table) })

    return processors


class ASCIINode(object):
    group = False
    dirty = True

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.init()


    def get_linecol(self):
        return textx.get_model(self)._tx_parser.pos_to_linecol(self._tx_position)


    def get_positions(self):
        return self._tx_position, self._tx_position_end


    def init(self):
        'late, extra initialisation'
        pass


    def debug(self):
        print(self.__dict__)


class MetaNode(ASCIINode):
    multiline = False
    sep = ''

    def printables(self, append_to=None):
        append_to = append_to or []
        return append_to


class CmdNode(ASCIINode):
    multiline = False
    label_type = None
    sep = ':'

    def __str__(self):
        return self.keyword


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.append(self.keyword.upper())
        return append_to


class NodeList(ASCIINode):
    sep = ','

    def __init__(self, **kwargs):
        self.parent = kwargs['parent']
        del kwargs['parent']
        self.args = list(kwargs.values())
        self.init()


def find_parent_type(type_, node):
    from hitbasic.models.default import Group
    def _find_type(type_, node):
        if node == None:
            return None
        if isinstance(node, type_):
            return node
        if not hasattr(node, 'parent'):
            return None
        return _find_type(type_, node.parent)

    if not hasattr(node, 'parent'):
        return None

    return _find_type(type_, node.parent)


Node = ASCIINode
