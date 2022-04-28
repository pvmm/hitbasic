# Control structures and related models


from hitbasic.helpers import string
from hitbasic.models import Node, CmdNode
from hitbasic.models.labels import LabelMark
from hitbasic.models.expressions import find_type, is_terminal, find_terminal, CmpOp
from hitbasic.models.conditions import IfThenStmt
from hitbasic.models.default import AttrStmt, Group
from hitbasic.exceptions import LineTooShort
from hitbasic import cfg


def processor(select_stmt, symbol_table):
    print("select_case.processor called")
    statements = []

    if is_terminal(select_stmt.expr):
        tmp = find_terminal(select_stmt.expr)
        symbol_table.check_hitbasic_var(tmp, throw_exception=not(cfg.no_decl))
        # If expression is already a simple variable, just use that.
        if tmp.lvalue:
            select_var = tmp
        else:
            # It's a literal value, which requires a variable.
            select_var = symbol_table.create_hitbasic_var(type = find_type(select_stmt.expr), inner=True)
    else:
        # Not a terminal, so we put it in a variable.
        select_var = symbol_table.create_hitbasic_var(type = find_type(select_stmt.expr), inner=True)
        statements.append(AttrStmt(select_var, select_stmt.expr))

    else_clause = False

    for case_clause in select_stmt.cases:
        if else_clause:
            raise ElseClauseError('case clause found after case-else clause')
        # format: Case Is <operator> <expr>
        if case_clause.expr.is_clause:
            # Operation with least priority in the expression
            cmp_op = case_clause.expr.is_clause.opr
            operator = case_clause.expr.is_clause.op1
            # 'Is' is a placeholder for select_var and will be replaced in code generation
            expr = cmp_op(select_var, operator)
            stmt = IfThenStmt(expr, case_clause.statements)
        # format: Case Else
        elif case_clause.expr.else_clause:
            if else_clause:
                raise ElseClauseError('case-else clause already defined')
            else_clause = True
            stmt = ElseClause(case_clause.statements)
        # default: Case <expression>
        else:
            # Operation with least priority in the expression
            expr = CmpOp(op1=select_var, opr='=', op2=case_clause.expr)
            stmt = IfThenStmt(expr, list(case_clause.statements))

        statements.append(stmt)

    return Group(statements)


class CaseClause(CmdNode):
    keyword = 'CASE'
    group = True

    def init(self):
        # Detect label inside code block
        for stmt in self.statements:
            if type(stmt) == LabelMark:
                self.multiline = True
                break


    def __iter__(self):
        return iter(self.statements)


class SelectStmt(CmdNode):
    keyword = 'SELECT'
    multiline = False
    group = True

    def __iter__(self):
        return iter(self.clauses)

