import os, pkgutil

modules = __all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
modules = list(__all__)

__all__ += [ 'modules' ]


def create_processors(symbol_table):
    return {
            'SelectStmt': lambda select_stmt: select_case.processor(select_stmt, symbol_table)
    }


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

    def debug(self):
        print(self.__dict__)

    def fits(self, available):
        return len(str(self)) < available

    def __bytes__(self):
        return self.keyword.upper()

    def write(self, file):
        pass


class ASCIINodeList(ASCIINode):
    def __init__(self, **kwargs):
        self.parent = kwargs['parent']
        del kwargs['parent']

        self.args = []
        for key, value in kwargs.items():
            self.args.append(value)
        self.init()


Node = ASCIINode
NodeList = ASCIINodeList
