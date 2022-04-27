'Declaration of dimensions (arrays) and scalar variables'

from io import StringIO

from hitbasic import cfg
from hitbasic.helpers.string import write_list
from hitbasic.msx.types import get_type_from_id
from hitbasic.models import Node, CmdNode


def processor(dim_stmt, symbol_table):
    for decl in dim_stmt.declarations:
        if get_type_from_id(decl.var.name):
            symbol_table.create_hitbasic_var(decl.var.name, ranges=decl.var.ranges)
        else:
            symbol_table.create_hitbasic_var(decl.var.name, type=decl.type, ranges=decl.var.ranges)
    return dim_stmt


class DimRangeDecl(Node):
    def __str__(self):
        if self.begin:
            return f'{self.end}-{self.begin}'
        else:
            return f'{self.end}'


class DimVarDecl(Node):
    def __str__(self):
        if not self.var.ranges:
            return f'{self.var.name}'
        else:
            ranges = write_list(self.var.ranges)
            return f'{self.var.name}({ranges})'


class DimStmt(CmdNode):
    keyword = 'Dim'

    def printables(self, append_to=None):
        append_to = append_to or []
        tmp = []

        for decl in self.declarations[1:]:
            tmp.append(f'{decl}')

        tmp.insert(0, f'{self.keyword}{cfg.spacing}%s' % self.declarations[0])
        append_to.extend(tmp)

        return append_to

