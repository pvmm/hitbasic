# Declaration of dimensions (arrays) and scalar variables

from io import StringIO

from hitbasic import cfg
from hitbasic.msx import types
from hitbasic.models import Node, CmdNode, find_parent_type
from hitbasic.models.expressions import RValue
from hitbasic.models.group import Group
from hitbasic.models.default import AssignStmt, RValue
from hitbasic.helpers import debug
from hitbasic.helpers.string import write_list


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
        type_ = types.get_type_from_id(self.var.identifier)
        var = symbol_table.create_hitbasic_var(type_=type_, inner=True)
        mapping = (var, RValue(var=self.var))

        # Mark assignment position in the source code
        if hasattr(stmt, '_var_mapping'):
            stmt._var_mapping.append(mapping)
        else:
            stmt._var_mapping = [mapping]

        return var


class DimRangeDecl(Node):
    def __str__(self):
        if self.begin:
            return f'{self.end - self.begin}'
        else:
            return f'{self.end}'


class DimNameDecl(Node): pass
#    def __str__(self):
#        print(self.identifier)
#        1/0


class DimTypedDecl(Node): pass


class DimVarDecl(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def __str__(self):
        if not self.var.ranges:
            return f'{self.ref}'
        else:
            ranges = write_list(self.var.ranges)
            return f'{self.ref}({ranges})'


    def get_type(self):
        return self.type if self.type else types.get_type_from_id(self.var.identifier)


    def processor(self, symbol_table):
        self.ref = symbol_table.create_hitbasic_var(self.var.identifier, type_=self.get_type(), ranges=self.var.ranges)
        debug("DimVarDecl: declaring variable %s (%s) of type %s in the symbol table" % (self.var.identifier, self.ref, self.get_type()))
        return self


class DimStmt(CmdNode):
    keyword = 'Dim'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def processor(stmt, symbol_table):
        if stmt.declarations:
            group = Group()
            group.append(stmt)

            for decl in stmt.declarations:
                if decl.expr:
                    group.append(AssignStmt(decl, decl.expr, parent=stmt))

            return group

        return stmt


    def printables(self, append_to=None):
        append_to = append_to or []
        tmp = []

        for decl in self.declarations[1:]:
            tmp.append(f'{decl}')

        tmp.insert(0, f'{self.keyword}{cfg.spacing}%s' % self.declarations[0])
        append_to.extend(tmp)

        return append_to

