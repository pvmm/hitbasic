"Anything else goes here"


from hitbasic.helpers.list import flatten
from hitbasic import cfg
from hitbasic.models import CmdNode, Node


class VarDefn(Node): pass


class AttrStmt(CmdNode):
    def __init__(self, definition, value=None, **kwargs):
        super().__init__(**kwargs)
        if type(definition) == VarDefn:
            self.var = definition.var
            self.value = definition.expr
        else:
            self.var = definition
            self.value = value


    def printables(self, append_to=[]):
        append_to.extend([f"{self.var}{cfg.arg_spacing}={cfg.arg_spacing}{self.value}"])
        return append_to


class Group(CmdNode):
    group = True

    def __init__(self, statements):
        self.statements = statements


    def __iter__(self):
        return iter(self.statements)


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.extend(flatten([stmt.printables() for stmt in self.statements]))
        return append_to
