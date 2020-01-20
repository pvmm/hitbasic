from contextlib import suppress

from ..helper import *
from ..exceptions import *


class PrintVisitor:

    def __init__(self):
        pass


    def visit_print_stmt(self, node, children):
        statement, fileno, [*params] = children
        if fileno:
            return self.create_statement(statement, params=(fileno, *params))
        return self.create_statement(statement, params=params, arg_sep=())


    def visit_print_params(self, node, children):
        return children[0]


    def visit_print_fileno(self, node, children):
        [fileno] = children
        return self.create_clause('fileno', fileno=fileno)


    def visit_print_using_fmt(self, node, children):
        fmt, arg_list = children
        return self.create_clause('using', format=fmt, params=arg_list),


    def visit_print_exprs(self, node, children):
        return children


    def visit_print_expr(self, node, children):
        [expr] = children
        return expr


    def visit_print_sep(self, node, children):
        return self.create_token(children[0])

