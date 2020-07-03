from contextlib import suppress

from .. import language_clauses as clauses

from .decorator import store_node
from ..helper import *
from ..exceptions import *


class StructureVisitor:

    def expand_case_op(self, var, expr):
        if isinstance(expr, clauses.case_op):
            return self.create_operation(expr.op, var, expr.op2, node=expr.op2)
        elif expr.op.title() == 'To':
            op1 = self.create_operation('>=', var, expr.op1, node=expr)
            op2 = self.create_operation('<=', var, expr.op2, node=expr)
            return self.create_operation('And', op1, op2, node=expr)
            #return self.create_unary_op('Not', tmp, node=expr)
        raise SyntaxError('case has no reference to selector variable')


    @store_node
    def visit_select_stmt(self, node, children):
        selector, *cases  = children
        var = self.symbol_table.create_hitbasic_var(type=selector.type)
        ref = self.create_reference(var, node=selector)
        code_block = []
        code_block.append(self.create_attribution(ref, selector, node=node[1]))
        for case in cases:
            if not isinstance(case, clauses.case):
                pos = case.position
                linecol = self.parser.pos_to_linecol(pos)
                raise SelectCaseError(case, linecol)
            old_expr = None
            for expr in case.params:
                print('expr =', expr.translate())
                expr = self.expand_case_op(ref, expr)
                if old_expr:
                    expr = self.create_operation('Or', old_expr, expr, node=expr)
                    print('new_expr =', expr.translate())
                old_expr = expr
            if old_expr: # Case Is
                expr = self.create_operation('Or', old_expr, expr, node=expr)
                #expr = self.create_unary_op('Not', old_expr)
                expr = self.visit_not_op(old_expr, ['Not', old_expr])
                code_block.append(self.visit_if_then_else_stmt(case, [expr, flatten(case.code_block)]))
            else: # Case Else
                code_block.append(self.create_statement('Multiple', code_block=flatten(case.code_block)))
        return self.create_statement('Multiple', code_block=code_block)


    def visit_select_case(self, node, children):
        params, _, code_block = children
        params = flatten(params)
        return self.create_clause('case', case_type=clauses.CASE_IS, params=params, code_block=code_block)


    def visit_select_case_else(self, node, children):
        _, code_block = children
        return self.create_clause('case', case_type=clauses.CASE_ELSE, code_block=code_block)


    def visit_case_exprs(self, node, children):
        return children


    def visit_case_comparison(self, node, children):
        _, op2 = children
        comparator = node[1][0][0]
        cmp_kw = comparator.flat_str()
        return self.create_case_op(cmp_kw, op2, node=node[1])


    def visit_case_interval(self, node, children):
        return self.create_operation('To', children[0], children[1], node=node)


    def visit_case_value(self, node, children):
        'Case 3 is the same as Case Is = 3'
        op2, = children
        return self.create_case_op('=', op2, node=children[0])


    def visit_case_block(self, node, children):
        return children

