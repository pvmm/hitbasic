"Anything else goes here"


from hitbasic import cfg
from hitbasic.models import Node, MetaNode, CmdNode, find_parent_type
from hitbasic.models.expressions import RValue
from hitbasic.models.group import Group
from hitbasic.helpers.list import flatten, interleave
from hitbasic.msx.types import get_type_from_id


class VarDefn(Node): pass


class AssignStmt(CmdNode):
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


class Program(Group):
    pass


def processor(node, symbol_table):
    'statement processor'
    if not isinstance(node, CmdNode):
        return node

    if node.group:
        it = iter(node)

        for pos, stmt in enumerate(it):
            if hasattr(stmt, '_var_mapping'):
                for var, expr in stmt._var_mapping:
                    node.insert(pos, AssignStmt(var, expr, parent=node))
                    stmt = next(it)

    return node

