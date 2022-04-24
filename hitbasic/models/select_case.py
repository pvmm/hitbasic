# Control structures and related models


from hitbasic.helpers import string
from hitbasic.models import Node, find_type
from hitbasic import cfg


def processor(select_stmt, symbol_table):
    print("select_case.processor called")
    if_stmts = []

    if select_stmt.expr.is_lvalue:
        # If expression is already a variable, just use that.
        select_var = find_terminal(select_stmt.expr)
    else:
        # Otherwise, define a new one.
        select_var = symbol_table.create_hitbasic_var(type = find_type(select_stmt.expr), temporary=True)
        if_stmts.append(AttrStmt(select_var, select_stmt.expr))

    else_clause = False

    for case_clause in select_stmt.cases:
        if else_clause:
            raise ElseClauseError('case clause found after case-else clause')
        # format: Case Is <operator> <expr>
        if case_clause.is_clause:
            # Operation with least priority in the expression
            cmp_op = case_clause.expr.comparator
            operator = case_clause.expr.operator
            # 'Is' is a placeholder for select_var and will be replaced in code generation
            expr = cmp_op(select_var, operator)
            if_stmt = IfStmt(expr, case_clause.statements)
        # format: Case Else
        elif case_clause.else_clause:
            if else_clause:
                raise ElseClauseError('case-else clause already defined')
            else_clause = True
            cmp_op = case_clause.expr.comparator
            # Comparators can be used as expressions
            expr = cmp_op(case_clause.expr.op1, case_clause.expr.op2)
            if_stmt = IfStmt(expr, case_clause.statements)
        # default: Case <expression>
        else:
            # Operation with least priority in the expression
            expr = case_clause.expr
            if_stmt = IfStmt(expr, case_clause.statements)

        if_stmts.append(if_stmt)

    return CodeBlock(if_stmts)
