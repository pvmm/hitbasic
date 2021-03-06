import sys
import re
import inspect

from os import path
from contextlib import suppress
from arpeggio import PTNodeVisitor, NonTerminal, visit_parse_tree, NoMatch

from .decorator import store_node
from .factory import FactoryProxy
from .statement import StatementVisitor
from .declaration import DeclarationVisitor
from .expression import ExpressionVisitor
from .conditional import ConditionalVisitor
from .loop import LoopVisitor
from .structure import StructureVisitor
from .printer import PrintVisitor

from ..factory import SurrogateFactory
from ..symbol_table import SymbolTable
from ..helper import *
from ..exceptions import *
from ..translations import CodeComponents

from .. import hitbasic
from .. import vars
from .. import language_types as types
from .. import language_tokens as tokens
from .. import language_statements as statements
from .. import language_subroutines as subroutines


class MSXBasicVisitor(StatementVisitor,
                      DeclarationVisitor,
                      ExpressionVisitor,
                      LoopVisitor,
                      StructureVisitor,
                      PrintVisitor,
                      ConditionalVisitor,
                      FactoryProxy,
                      PTNodeVisitor):

    def __init__(self, parser, **kwargs):
        parser = kwargs.pop('parser', parser)
        begin_line = kwargs.pop('begin_line', 10)

        PTNodeVisitor.__init__(self, **kwargs)
        FactoryProxy.__init__(self)
        PrintVisitor.__init__(self)
        DeclarationVisitor.__init__(self)
        LoopVisitor.__init__(self)

        self.parser = parser
        self.begin_line = begin_line
        self.debug = kwargs.pop('debug', False)
        self.pp_flag = kwargs.pop('pp', False) # Pretty-print deactivated by default
        self.arch = 'msx2+' # TODO: set this from an option received from argparse
        self.basic_ver = kwargs.pop('basic-ver', 2)

        # Scratchpad
        self.scratchpad = { 'var_list': [] }
        self.context = '_global'
        self.ret_var_count = 0

        # Symbol table
        self.symbol_table = SymbolTable()

        # Common program elements
        self.begin_label = self.create_statement('Label', identifier='BeginProgram', line_number=
                self.begin_line, pos=0)
        self.symbol_table.store_label(self.begin_label)

    ### Rules ###

    def visit_program(self, node, children):
        children = flatten(children)

        # Create finishing label (EndProgram)
        self.end_label = self.create_statement('Label', identifier='EndProgram', pos=node.position_end)
        self.symbol_table.store_label(self.end_label)

        # Find subroutines in the program and move them to the end.
        functions = [child for child in children if type(child) == subroutines.subroutine_type]
        main = [child for child in children if type(child) != subroutines.subroutine_type]

        # Insert labels at right positions
        main.insert(0, self.begin_label)
        main.append(self.end_label)
        main.append(self.create_statement('End'))
        program = main + functions

        try:
            code = CodeComponents(program).translate().freeze()
        except DimInitAccessError as e:
            raise self.put_location(e, pos=child.position)
        return self.symbol_table, code


    def visit_label_stmt(self, node, children):
        return children


    @store_node
    def visit_label_addr(self, node, children):
        [identifier, *_] = children
        try:
            label = self.create_label(identifier)
            self.symbol_table.store_label(label)
        except NameError:
            raise self.create_exception(NameNotDeclared, identifier)
        return label


    def visit_function_stmt(self, node, children):
        [identifier, params, type], body = children

        # Add function's entry point
        body.insert(0, self.create_label('%s()' % identifier, pos=node.position))

        # TODO: come up with a better job of detecting dangling codepaths
        #if body[-1] != statements.Statement('Return'):
        if isinstance(body[-1], statements.TYPES['Default']) and body[-1] == 'Return':
            body.append(self.create_statement('Return', node=body[-1]))

        # Store function in symbol table and return Function object
        identifier = '%s()' % identifier
        self.symbol_table.register_function(identifier, params=params, type=type)
        return self.create_subroutine(body)


    def visit_func_head1(self, node, children):
        identifier, params, ret_type = children
        self.symbol_table.create_hitbasic_var(identifier, type=ret_type)
        return identifier, params, ret_type


    def visit_func_head2(self, node, children):
        identifier, params = children
        ret_type = types.get_type_from_identifier(identifier)
        self.symbol_table.create_hitbasic_var(identifier, type=ret_type)
        return identifier, params, ret_type


    def visit_func_return_type(self, node, children):
        return types.get_type_from_type_id(*children)


    def visit_func_vars(self, node, children):
        return tuple(children)


    def visit_func_var_decl(self, node, children):
        if tokens.Token('As') in children:
            identifier, _, type_name = children
            type = types.get_type_from_type_id(type_name)
            return self.symbol_table.create_hitbasic_var(identifier, type=type)
        else:
            identifier, type_name = children
            type = types.get_type_from_type_id(type_name)
            return self.symbol_table.create_hitbasic_var(identifier, type=type)


    def visit_func_body_stmt(self, node, children):
        result = children.pop()
        return result


    def visit_func_body(self, node, children):
        result = []
        # Remove dangling separators
        for index, child in enumerate(children):
            if child == ':' or child == '\n': continue
            result.append(child)
        if len(result) > 1:
            result, tail = [result[0]], result[1]
            result.extend(tail)
        return result


    def visit_func_exit_stmt(self, node, children):
        return self.create_statement('Return')


    def visit_func_end_stmt(self, node, children):
        return None


    def visit_comma_sep_adrs(self, node, children):
        return parse_arg_list(children)


    def visit_address(self, node, children):
        return children.pop()


    def visit_type_des(self, node, children):
        return node.flat_str()


    def visit_str_type_des(self, node, children):
        return node.flat_str()


    def visit_num_type_des(self, node, children):
        return node.flat_str()


    def visit_alphanum_name(self, node, children):
        return node.flat_str()


    @store_node
    def visit_var(self, node, children):
        [(identifier, params)] = children
        if type(params) == list: identifier += '()'
        if not (var := self.symbol_table.check_id(identifier, params)):
            raise self.create_exception(NameNotDeclared, identifier)
        return self.create_reference(var, params)


    def decompose(self, identifier):
        'Break variable in smaller components and operations, like "Axorb" could become A xor B.'
        known_vars = self.symbol_table.get_hitbasic_vars()
        known_vars.sort()
        var_parser = vars.create_var_parser(known_vars)
        with suppress(NoMatch):
            return var_parser.parse(identifier)


    @store_node
    def visit_rvalue(self, node, children):
        [(identifier, params)] = children
        if type(params) == list: identifier += '()'
        var = self.symbol_table.check_id(identifier, params)
        tree = self.decompose(identifier)
        if var and not isinstance(var, types.BuiltIn):
            if var and tree and tree.flat_str() != identifier:
                var_list = [x.flat_str() for x in flatten(tree)]
                expr = ' '.join(var_list).strip()
                raise self.create_exception(AmbiguousCode, identifier, expr)
        elif not var and tree:
            code = visit_parse_tree(tree, ExpressionVisitor(symbol_table=self.symbol_table))
            return self.visit_expr(tree, code)
        if not var:
            raise self.create_exception(NameNotDeclared, identifier)
        else:
            return self.create_reference(var, params)


    def visit_array(self, node, children):
        return children


    def visit_array_name(self, node, children):
        identifier = children
        return ''.join(identifier)


    def visit_array_args(self, node, children):
        if len(children) == 0:
            return children
        [[*args]] = children
        return args


    def visit_scalar(self, node, children):
        identifier = children
        return ''.join(identifier), None


    def visit_trailing_spaces(self, node, children):
        return None


    def visit_new_line(self, node, children):
        return None
