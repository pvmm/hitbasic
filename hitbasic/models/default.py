"Anything else goes here"


from hitbasic import cfg
from hitbasic.models import Node, MetaNode, CmdNode
from hitbasic.models.simple import SimpleStmt
from hitbasic.helpers.list import flatten, interleave
from hitbasic.msx.types import get_type_from_id


class VarDefn(Node): pass


class AttrStmt(CmdNode):
    keyword = 'LET'

    def __init__(self, definition, value=None, **kwargs):
        super().__init__(**kwargs)
        if type(definition) == VarDefn:
            self.var = definition.var
            self.value = definition.expr
        else:
            self.var = definition
            self.value = value


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.extend([f"{self.var}{cfg.arg_spacing}={cfg.arg_spacing}{self.value}"])
        return append_to


class Group(CmdNode):
    group = True
    sep = f'{cfg.arg_spacing}:{cfg.arg_spacing}'

    def __init__(self, statements, **kwargs):
        super().__init__(**kwargs)
        self.statements = statements


    def insert(self, pos, stmt):
        self.statements.insert(pos, stmt)


    def __iter__(self):
        return iter(self.statements)


    def printables(self, append_to=None):
        append_to = append_to or []
        tmp = interleave([stmt.printables() for stmt in self], self.sep)
        append_to.extend(flatten(tmp))
        return append_to


class Program(Group):
    pass


def processor(node, symbol_table):
    'statement processor'
    if not isinstance(node, CmdNode):
        return node

    if node.group:
        it = iter(node)

        for pos, stmt in enumerate(it):
            if hasattr(stmt, '_func_mapping'):
                for var, func_call in stmt._func_mapping:
                    node.insert(pos, AttrStmt(var, func_call, parent=node))
                    stmt = next(it)

    return node

