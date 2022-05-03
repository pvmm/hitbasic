# Control structures and related models


from hitbasic import cfg
from hitbasic.helpers.list import flatten, interleave
from hitbasic.models.expressions import Expression
from hitbasic.models import CmdNode
from hitbasic.models.group import Group
from hitbasic.models.meta import EOL
from hitbasic.models.default import Group


class CaseExpr(Expression): pass


class ThenClause(Group):
    keyword = 'THEN'
    sep = f'{cfg.arg_spacing}:{cfg.arg_spacing}'

    def printables(self, append_to=None):
        append_to = append_to or []
        tmp = flatten([stmt.printables() for stmt in self.statements])
        append_to.extend(interleave(tmp, self.sep))
        return append_to


class ElseClause(Group):
    keyword = 'ELSE'
    sep = f'{cfg.arg_spacing}:{cfg.arg_spacing}'

    def printables(self, append_to=None):
        append_to = append_to or []
        tmp = flatten([stmt.printables() for stmt in self.statements])
        append_to.extend([cfg.spacing, self.keyword, cfg.spacing] + interleave(tmp, self.sep))
        return append_to


class IfThenStmt(Group):
    keyword = 'IF3'
    group = True

    def __init__(self, expr, statements, **kwargs):
        statements = [ThenClause(kwargs['then_stmts']), EOL()]
        super().__init__(statements, **kwargs)
        self.expr = expr
        self.statements = statements


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.append(f'{self.keyword}{cfg.spacing}{self.expr}{cfg.spacing}THEN')
        append_to.extend([cfg.spacing] + flatten([stmt.printables() for stmt in self.statements]))
        return append_to


class IfThenElseStmt(Group):
    keyword = 'IF'

    def __init__(self, **kwargs):
        statements = [ThenClause(kwargs['then_stmts']), ElseClause(kwargs['else_stmts']), EOL()]
        super().__init__(statements, **kwargs)


    def processor(self, symbol_table):
        return self


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.append(f'{self.keyword}{cfg.spacing}{self.expr}{cfg.spacing}THEN')
        append_to.extend([cfg.spacing] + flatten([stmt.printables() for stmt in self.statements]))
        return append_to


class IfThenOneLiner(IfThenStmt):
    keyword = 'IF4'


class IfThenElseOneLiner(IfThenElseStmt):
    keyword = 'IF5'

