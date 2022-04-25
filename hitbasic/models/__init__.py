import os, pkgutil

from hitbasic import msx
from hitbasic.exceptions import LineTooShort

modules = __all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
modules = list(__all__)

__all__ += [ 'modules' ]


def create_processors(symbol_table):
    return {
            'SelectStmt': lambda select_stmt: select_case.processor(select_stmt, symbol_table)
    }


class ASCIINode(object):
    group = False
    dirty = True

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.init()


    def init(self):
        'later initialisation'
        pass


    def debug(self):
        print(self.__dict__)


class ASCIICmdNode(ASCIINode):
    multiline = False
    label_type = None

    def __str__(self):
        return self.keyword


class ASCIINodeList(ASCIINode):
    def __init__(self, **kwargs):
        self.parent = kwargs['parent']
        del kwargs['parent']
        self.args = list(kwargs.values())
        self.init()


Node = ASCIINode
CmdNode = ASCIICmdNode
NodeList = ASCIINodeList
