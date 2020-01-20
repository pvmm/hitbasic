from contextlib import suppress

from ..helper import *
from ..exceptions import *


class StructureVisitor:

    def visit_select_stmt(self, node, children):
        selector, _ = children.pop(0), children.pop(0)
        for case in children:
            if not isinstance(case, CaseClause):
                pos = case.position if isinstance(case, Node) else node.position
                linecol = self.parser.pos_to_linecol(pos)
                raise SelectCaseError(case, linecol)
        return create_select_statement(selector, children, node=node)


    def visit_select_case(self, node, children):
        operations, _, block = children
        operations = flatten(operations)
        return create_case_clause(operations, block, node=node)


    def visit_select_case_else(self, node, children):
        _, block = children
        return create_case_clause(create_keyword('Else', node=node[1]), block,
                node=node)


    def visit_case_block2(self, node, children):
        return children


    def visit_case_exprs(self, node, children):
        return children


    def visit_case_comparison(self, node, children):
        comparator = node[1][0][0]
        comparator_kw = create_keyword(comparator.flat_str(), node=comparator)
        is_kw = create_keyword('Is', node=node)
        op2 = children[1]
        return create_operation(comparator_kw, is_kw, op2, node=node)


    def visit_case_interval(self, node, children):
        return create_operation('To', children[0], children[1], node=node)


    def visit_case_value(self, node, children):
        return create_operation('=', create_keyword('Is', node=node),
                children[0], node=children[0])

