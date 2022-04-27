# Control structures and related models


from hitbasic import cfg
from hitbasic.models.expressions import Expression
from hitbasic.models.default import Group
from hitbasic.models import CmdNode


class CaseExpr(Expression): pass


class ElseClause(Group):
    keyword = 'ELSE'


class EndIfClause(CmdNode):
    keyword = 'ENDIF'


class IfThenStmt(CmdNode):
    keyword = 'IF'
    def __init__(self, expr, statements):
        self.expr = expr
        self.statements = statements


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.append(f'{self.keyword}{cfg.spacing}{self.expr}{cfg.spacing}THEN')
        append_to.extend([stmt.printables() for stmt in self.statements])
        append_to.append(EndIfClause())
        return append_to


class IfThenElseStmt(IfThenStmt):
    keyword = 'IF'
    def __init__(self, expr, then_stmts, else_stmts):
        self.expr = expr
        self.statements = []
        self.statements.extend(then_stmts)
        self.statements.append(ElseClause())
        self.statements.extend(else_stmts)
        self.statements.append(EndIfClause())


class IfThenOneLiner(IfThenStmt):
    def printables(self, append_to=None):
        raise NotImplemented


class IfThenElseOneLiner(IfThenElseStmt):
    def printables(self, append_to=None):
        raise NotImplemented

