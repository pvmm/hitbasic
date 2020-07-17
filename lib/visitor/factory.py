from ..factory import factory
from ..exceptions import *

from .. import language_clauses as clauses
from .. import language_statements as statements


class FactoryProxy:
    def __init__(self):
        self.current_node = None
        self.current_rule = None


    def create_token(self, *token, **kwargs): # *token allow a compound token
        node = kwargs.pop('node', self.current_node)
        return factory.create_token(*token, node=node, **kwargs)


    def create_reference(self, value, params=None, **kwargs):
        node = kwargs.pop('node', self.current_node)
        return factory.create_reference(value, params, node=node, **kwargs)


    def create_nil(self, **kwargs):
        node = kwargs.pop('node', self.current_node)
        return factory.create_nil(node=node, **kwargs)


    def create_literal(self, value, type, **kwargs):
        node = kwargs.pop('node', self.current_node)
        return factory.create_literal(value, type, node=node, **kwargs)


    def create_sep_list(self, *args, sep=',', list_type=clauses.REGULAR, **kwargs):
        node = kwargs.pop('node', self.current_node)
        return factory.create_sep_list(*args, sep=sep, list_type=list_type, node=node, **kwargs)


    def create_clause(self, clause, **kwargs):
        node = kwargs.pop('node', self.current_node)
        return factory.create_clause(clause, node=node, **kwargs)


    def create_unary_op(self, op, operand, need_parens=False, **kwargs):
        node = kwargs.pop('node', self.current_node)
        try:
            return factory.create_unary_op(op, operand, need_parens, node=node, **kwargs)
        except TypeMismatch as e:
            raise e.set_location(self.parser.file_name, self.parser.context(position=node.position),
                                 self.parser.pos_to_linecol(node.position))


    def create_operation(self, op, op1, op2, need_parens=False, **kwargs):
        'legacy compatible shortcut'
        node = kwargs.pop('node', self.current_node)
        try:
            return factory.create_operation(op, op1, op2, need_parens, node=node, **kwargs)
        except TypeMismatch as e:
            raise e.set_location(self.parser.file_name, self.parser.context(position=node.position),
                                 self.parser.pos_to_linecol(node.position))


    def create_case_op(self, op, op2, need_rparens=False, **kwargs):
        node = kwargs.pop('node', self.current_node)
        try:
            return factory.create_case_op(op, op2, need_rparens, node=node, **kwargs)
        except TypeMismatch as e:
            raise e.set_location(self.parser.file_name, self.parser.context(position=node.position),
                    self.parser.pos_to_linecol(node.position))


    def create_tuple(self, *values, use_parentheses=False, **kwargs):
        'Create a n-tuple.'
        node = kwargs.pop('node', self.current_node)
        return factory.create_tuple(*values, node=node, use_parentheses=use_parentheses, **kwargs)


    def create_initialisation(self, dimensions, values, type, **kwargs):
        'Processes Dim initialisation expressions.'
        node = kwargs.pop('node', None)
        return factory.create_initialisation(dimensions, values, type, node=node, **kwargs)


    def create_range(self, begin, end, **kwargs):
        'Processes range clauses, like "1 to 20".'
        node = kwargs.pop('node', self.current_node)
        return factory.create_range(begin, end, node=node, **kwargs)


    def create_point(self, x, y, step, **kwargs):
        'Processes range clauses, like "1 to 20".'
        node = kwargs.pop('node', self.current_node)
        return factory.create_point(x, y, step, node=node, **kwargs)


    def create_box(self, *points, **kwargs):
        'Processes range clauses, like "1 to 20".'
        node = kwargs.pop('node', self.current_node)
        return factory.create_box(*points, node=node, **kwargs)


    def create_statement(self, tokens, **kwargs):
        node = kwargs.pop('node', self.current_node)
        return factory.create_statement(tokens, node=node, **kwargs)


    def create_attribution(self, lvalue, rvalue, **kwargs):
        node = kwargs.pop('node', self.current_node)
        return factory.create_attribution(lvalue, rvalue, node=node, **kwargs)


    def create_label(self, identifier, type=statements.INTERNAL, line_number=None, **kwargs):
        'legacy compatible shortcut'
        node = kwargs.pop('node', self.current_node)
        return factory.create_label(identifier, type=type, line_number=line_number, node=node, **kwargs)


    def create_subroutine(self, code_block, **kwargs):
        node = kwargs.pop('node', self.current_node)
        return factory.create_subroutine(code_block, node=node, **kwargs)


    def put_location(self, exception, pos=None):
        'insert location in exception for a reraise'
        return exception.set_location(self.parser.file_name, self.parser.context(pos),
                                      self.parser.pos_to_linecol(pos))


    def create_exception(self, exception_type, *args, **kwargs):
        'create exception with predefined location'
        node = kwargs.pop('node', self.current_node)
        pos = kwargs.pop('pos', node.position or None)
        raise exception_type(*args, filename=self.parser.file_name, context=self.parser.context(pos),
                             pos=self.parser.pos_to_linecol(pos))
