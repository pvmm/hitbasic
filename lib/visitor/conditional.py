from ..factory import SurrogateFactory
from ..symbol_table import SymbolTable
from ..helper import *
from ..exceptions import *

from .. import language_types as types
from .. import language_tokens as tokens
from .. import language_statements as statements
from .. import language_subroutines as subroutines


class ConditionalVisitor:

    def write_if_then_stmt(self, expr, then_clauses):
        # if label
        then_id = self.symbol_table.register_label(prefix='EndIf')
        then_label = self.create_statement('Label', identifier=then_id)
        self.symbol_table.store_label(then_label)

        # then_clauses subroutine
        then_clauses = flatten(then_clauses)
        then_clauses.append(then_label)
        then_subroutine = self.create_subroutine(then_clauses)
        then_branch = self.create_statement('Branch', target=self.create_clause('Label', identifier=then_id),
                branch_type=statements.GOTO)

        # wrapping it up!
        expr = self.visit_not_op(expr, ['Not', expr]) # invert condition so that the conditional and then-clauses
                                                      # are adjacent
        conditional = self.create_statement('Conditional', expression=expr, then_branch=then_branch)
        return self.create_statement('Multiple', code_block=(conditional, then_subroutine))


    def write_if_then_else_stmt(self, expr, then_clauses, else_clauses):
        # if label
        then_id = self.symbol_table.register_label(prefix='IfThen')
        then_label = self.create_statement('Label', identifier=then_id)
        self.symbol_table.store_label(then_label)

        # then_clauses subroutine
        then_clauses = flatten(then_clauses)
        then_clauses.insert(0, then_label)
        then_clauses.append(self.create_statement('Return'))
        then_subroutine = self.create_subroutine(then_clauses)
        then_branch = self.create_statement('Branch', target=self.create_clause('Label', identifier=then_id),
                branch_type=statements.GOSUB)

        # else_clauses routine
        else_name = self.symbol_table.register_label(prefix='IfElse')
        else_label = self.create_statement('Label', identifier=else_name)
        self.symbol_table.store_label(else_label)
        else_clauses = flatten(else_clauses)
        else_clauses.insert(0, else_label)
        else_clauses.append(self.create_statement('Return'))
        else_subroutine = self.create_subroutine(else_clauses)
        else_branch = self.create_statement('Branch', target=self.create_clause('Label', identifier=else_name),
                branch_type=statements.GOSUB)

        # wrapping it up!
        conditional = self.create_statement('Conditional', expression=expr, then_branch=then_branch,
                else_branch=else_branch)
        return self.create_statement('Multiple', code_block=(conditional, then_subroutine, else_subroutine))


    def visit_if_then_else_stmt(self, node, children):
        expr, instruction, *remaining = children
        if statements.contains(instruction, type='Goto'):
            then_branch = instruction
            else_branch, = remaining if remaining else (None,)
            return self.create_statement('Conditional', expression=expr, then_branch=then_branch,
                                         else_branch=else_branch)
        elif tokens.contains(instruction, type='Then'):
            try:
                then_clauses, *else_clauses = remaining
            except ValueError:
                then_clauses = else_clauses = []
            if not else_clauses:
                return self.write_if_then_stmt(expr, then_clauses)
            else:
                return self.write_if_then_else_stmt(expr, then_clauses, else_clauses)


    def visit_inln_then_clauses(self, node, children):
        return children.pop()


    def visit_inln_else_clauses(self, node, children):
        return children.pop()


    def visit_inln_stmts(self, node, children):
        return flatten(children)


    def visit_then_clauses(self, node, children):
        return children


    def visit_else_clauses(self, node, children):
        return children
