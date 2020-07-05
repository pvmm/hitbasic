import sys

from ..helper import *
from ..exceptions import *

from .. import language_statements as statements


class LoopVisitor:

    def __init__(self):
        self.loop_recorder = {}


    def save_loop(self, var):
        self.loop_recorder[var.value] = var


    def check_in_loop(self, var=None):
        if len(self.loop_recorder) == 0:
            return False
        if var and var.value in self.loop_recorder:
            return True
        return False


    def create_do_while(self, expr, code_block):
        start_identifier = self.symbol_table.register_label(prefix='DoLoopStart')
        start_label = self.create_label(start_identifier, type=statements.INTERNAL)
        self.symbol_table.store_label(start_label)
        continue_branch = self.create_statement('Branch', target=start_label, branch_type=statements.GOTO)

        end_identifier = self.symbol_table.register_label(prefix='DoLoopEnd')
        end_label = self.create_label(end_identifier, type=statements.INTERNAL)
        self.symbol_table.store_label(end_label)
        exit_branch = self.create_statement('Branch', target=end_label, branch_type=statements.GOTO)

        return self.create_statement('Do_While', expression=expr, code_block=flatten(code_block), start_label=
                start_label, end_label=end_label, exit_branch=exit_branch, continue_branch=continue_branch)


    def create_do_until(self, expr, code_block):
        identifier = self.symbol_table.register_label(prefix='DoLoopStart')
        start_label = self.create_label(identifier, type=statements.INTERNAL)
        self.symbol_table.store_label(start_label)
        continue_branch = self.create_statement('Branch', target=start_label, branch_type=statements.GOTO)

        identifier = self.symbol_table.register_label(prefix='DoLoopEnd')
        end_label = self.create_label(identifier, type=statements.INTERNAL)
        self.symbol_table.store_label(end_label)
        exit_branch = self.create_statement('Branch', target=end_label, branch_type=statements.GOTO)

        return self.create_statement('Do_Until', expression=expr, code_block=flatten(code_block), start_label=
                start_label, end_label=end_label, exit_branch=exit_branch, continue_branch=continue_branch)


    def create_loop_while(self, expr, code_block):
        loop_identifier = self.symbol_table.register_label(prefix='DoLoopStart')
        do_loop_start = self.create_label(loop_identifier, type=statements.INTERNAL)
        self.symbol_table.store_label(do_loop_start)
        loop_branch = self.create_statement('Branch', target=do_loop_start, branch_type=statements.GOTO)

        return self.create_statement('Loop_While', expression=expr, code_block=flatten(code_block), do_loop_start=
                do_loop_start, branch=loop_branch)


    def create_loop_until(self, expr, code_block):
        identifier = self.symbol_table.register_label(prefix='DoLoopStart')
        do_loop_start = self.create_label(identifier, type=statements.INTERNAL)
        self.symbol_table.store_label(do_loop_start)
        loop_branch = self.create_statement('Branch', target=do_loop_start, branch_type=statements.GOTO)

        return self.create_statement('Loop_Until', expression=expr, code_block=flatten(code_block), do_loop_start=
                do_loop_start, branch=loop_branch)


    def visit_do_loop_stmt(self, node, children):
        if len(node) == 6:
            if node[1][0].flat_str().title() == 'While':
                # Evalute while loop with condition at the beginning.
                (cond_type, expr), code_block = children
                return self.create_do_while(expr, flatten(code_block))
            if node[1][0].flat_str().title() == 'Until':
                # Evalute until loop with condition at the beginning.
                (cond_type, expr), code_block = children
                return self.create_do_until(expr, flatten(code_block))

            if node[5][0].flat_str().title() in 'While':
                # Evalute while loop with condition at the end.
                code_block, (cond_type, expr) = children
                return self.create_loop_while(expr, flatten(code_block))

            if node[5][0].flat_str().title() in 'Until':
                # Evalute until loop with condition at the end.
                code_block, (cond_type, expr) = children
                return self.create_loop_until(expr, flatten(code_block))
        raise SyntaxError()


    def visit_do_loop_cond(self, node, children):
        return children


    def visit_do_stmt_block(self, node, children):
        return children


    def visit_do_stmt(self, node, children):
        if len(children) == 0:
            return [self.create_statement(('Exit', 'Do'))]
        return children[0]


    def visit_for_stmt(self, node, children):
        var, (begin, end, step) = children
        assert var.value != None
        self.save_loop(var)
        return self.create_statement('For_Loop', var=var, begin=begin, end=end, step=step)


    def visit_next_stmt(self, node, children):
        if children: statement = self.create_statement('Next', params=children[0].pop())
        else: statement = self.create_statement('Next')
        if not statement.params and not self.check_in_loop():
            raise LoopNotFound(self.parser.context(statement.position),
                    self.parser.pos_to_linecol(statement.position))
        for var in iter(statement.params):
            try:
                if not self.check_in_loop(var):
                    raise LoopNotFound(self.parser.context(node.position),
                            self.parser.pos_to_linecol(node.position))
            except KeyError:
                raise LoopMismatch(self.parser.context(node.position),
                        self.parser.pos_to_linecol(node.position))
        return statement


    def visit_next_vars(self, node, children):
        return children


    def visit_next_var(self, node, children):
        [(identifier, params)] = children
        if params: identifier = '%s()' % identifier
        try:
            ref = self.symbol_table.get_hitbasic_var(identifier)
        except NameNotDeclared as e:
            context = self.parser.context(node[0].position)
            pos = self.parser.pos_to_linecol(node[0].position)
            raise e.set_location(self.filename, context, pos)
        return self.create_reference(ref, params, reference=ref)


    def visit_for_range_decl(self, node, children):
        try:
            begin, end, step = children
        except ValueError:
            (begin, end), step = children, 1
        return begin, end, step


    def visit_for_var(self, node, children):
        [(identifier, params)] = children
        if params: identifier = '%s()' % identifier
        ref = self.symbol_table.check_hitbasic_var(identifier)
        if not ref and self.no_dim_flag:
            return self.create_variable(identifier, params, reference=ref)
        if not ref:
            context = self.parser.context(node[0].position)
            pos = self.parser.pos_to_linecol(node[0].position)
            raise NameNotDeclared(identifier, context, pos)
        else:
            return self.create_reference(ref, params, reference=ref)
