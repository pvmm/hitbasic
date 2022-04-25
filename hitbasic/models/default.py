"Anything else goes here"

from hitbasic.models import CmdNode, Node


class VarDefn(Node):
    pass


class AttrStmt(CmdNode):
    def __init__(self, definition, value=None):
        if type(definition) == VarDefn:
            self.var = definition.var
            self.value = definition.expr
        else:
            self.var = definition
            self.value = value


class Group(CmdNode):
    def __init__(self, statements):
        self.statements = statements
