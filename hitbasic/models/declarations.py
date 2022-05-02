'Declaration of dimensions (arrays) and scalar variables'

from io import StringIO

from hitbasic import cfg
from hitbasic.msx import types
from hitbasic.models import Node, CmdNode
from hitbasic.helpers.string import write_list


class DimRangeDecl(Node):
    def __str__(self):
        if self.begin:
            return f'{self.end}-{self.begin}'
        else:
            return f'{self.end}'


class DimVarDecl(Node):
    def __str__(self):
        if not self.var.ranges:
            return f'{self.var.identifier}'
        else:
            ranges = write_list(self.var.ranges)
            return f'{self.var.identifier}({ranges})'


class DimStmt(CmdNode):
    keyword = 'Dim'

    def processor(self, symbol_table):
        for decl in self.declarations:
            if types.get_type_from_id(decl.var.identifier):
                symbol_table.create_hitbasic_var(decl.var.identifier, ranges=decl.var.ranges)
            else:
                type_ = decl.type if decl.type else types.default_type
                symbol_table.create_hitbasic_var(decl.var.identifier, type_=type_, ranges=decl.var.ranges)
        return self


    def printables(self, append_to=None):
        append_to = append_to or []
        tmp = []

        for decl in self.declarations[1:]:
            tmp.append(f'{decl}')

        tmp.insert(0, f'{self.keyword}{cfg.spacing}%s' % self.declarations[0])
        append_to.extend(tmp)

        return append_to

