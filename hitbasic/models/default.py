"Anything else goes here"


from hitbasic import cfg
from hitbasic.models import Node, MetaNode, CmdNode, find_parent_type
from hitbasic.models.expressions import RValue
from hitbasic.helpers.list import flatten, interleave
from hitbasic.msx.types import get_type_from_id


class VarDefn(Node): pass


class LValue(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def __str__(self):
        return f'{self.var}'


    def processor(self, symbol_table):
        # Find statement this expression belongs to
        stmt = find_parent_type(CmdNode, self)
        assert stmt, "expected statement that contains this expression was not found"

        # Create temporary variable for assignment
        type_ = get_type_from_id(self.var.identifier)
        var = symbol_table.create_hitbasic_var(type_=type_, inner=True)
        mapping = (var, RValue(var=self.var))

        # Mark assignment position in the source code
        if hasattr(stmt, '_var_mapping'):
            stmt._var_mapping.append(mapping)
        else:
            stmt._var_mapping = [mapping]

        return var


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


class Group(CmdNode):
    group = True
    sep = f'{cfg.arg_spacing}:{cfg.arg_spacing}'

    def __init__(self, statements=None, **kwargs):
        super().__init__(**kwargs)
        self.statements = statements or []


    def insert(self, pos, stmt):
        self.statements.insert(pos, stmt)


    def append(self, stmt):
        self.statements.append(stmt)


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
            if hasattr(stmt, '_var_mapping'):
                for var, expr in stmt._var_mapping:
                    node.insert(pos, AssignStmt(var, expr, parent=node))
                    stmt = next(it)

    return node

