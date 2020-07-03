import os

from os import path
from glob import glob
from importlib import import_module
from arpeggio import Terminal

from ..helper import *
from ..hitbasic import Surrogate
from ..exceptions import *

from .. import language_tokens as tokens
from .. import language_types as types
from .. import language_clauses as clauses
from .. import language_statements as statements
from .. import language_subroutines as subroutines
from .. import NO_RULE


def subc(module, cls_name):
    'remove unnecessary bits of a module class and turn it into a dictionary'
    subcls = dict(module.__dict__[cls_name].__dict__)
    remove = ['__module__', '__dict__', '__weakref__', '__doc__' ]
    for r in remove:
        with suppress(KeyError):
            del subcls[r]
    return subcls


class SurrogateFactory:
    'Make surrogate easier to track by merging it with the visitor'
    def __init__(self):
        self.current_node = None
        self.current_rule = None


    # TODO: move some of these initialisations to language_* files
    def create_factory_types(self):
        if hasattr(self, 'module'): return
        self.module = {}
        self.types = {}
        self.clause_type = {}
        self.statement_type = {}

        modules_path = path.dirname(path.realpath(__file__))
        modules = glob(path.join(modules_path, '..', 'translations', '*.py'))

        for module_name in modules:
            split_name = module_name.split(os.sep)
            if split_name[-1] == '__init__.py': continue
            key = split_name[-1].replace('.py', '')
            module_path = 'lib.%s.%s' % (split_name[-2], split_name[-1].replace('.py', ''))
            self.module[key] = import_module(module_path)

        # Allow creation of literals outside factory.
        self.types['String'] = type('String', (Surrogate,), subc(self.module['string_literal'], 'Type'))
        types.register( 'String', self.types['String'])
        self.types['Integer'] = type('Integer', (Surrogate,), subc(self.module['numeric_literal'], 'Type'))
        types.register('Integer', self.types['Integer'])
        self.types['Double'] = type('Double', (Surrogate,), subc(self.module['numeric_literal'], 'Type'))
        types.register('Double', self.types['Double'])
        self.types['Single'] = type('Single', (Surrogate,), subc(self.module['numeric_literal'], 'Type'))
        types.register('Single', self.types['Single'])
        self.types['Boolean'] = type('Boolean', (Surrogate,), subc(self.module['numeric_literal'], 'Type'))
        types.register('Boolean', self.types['Boolean'])

        for module_name, module in dict(filter(lambda i: i[0].endswith('_clause'), self.module.items())).items():
            clause = module_name.replace('_clause', '')
            self.clause_type[clause] = type('Clause(%s)' % clause, (Surrogate,), subc(module, 'Clause'))
            clauses.register(clause, self.clause_type[clause])

        self.initialisation_type = type('Initialisation', (Surrogate,), {})

        for module_name, module in dict(filter(lambda i: i[0].endswith('_statement'), self.module.items())).items():
            statement = module_name.replace('_statement', '')
            tokens = statement.split('_')
            statement = statement.title()
            self.statement_type[statement] = type('Statement(%s)' % statement, (Surrogate,), subc(module, 'Statement'))
            # Allow creation of statements outside factory.
            statements.register(statement, self.statement_type[statement])

        for key in statements.SIMPLE_STATEMENTS:
            tokens = make_tuple(key)
            statement = ' '.join(tokens)
            class_body = subc(self.module['simple_statements'], 'Statement')
            class_body.update({'tokens': tuple(token.upper() for token in tokens)})
            self.statement_type[statement] = type('Statement(%s)' % statement, (Surrogate,), class_body)
            # Allow creation of statements outside factory.
            statements.register(statement, self.statement_type[statement])

        # more sofisticated language constructs
        self.subroutine_type = subroutines.subroutine_type #type('Subroutine', (Surrogate,), self.module['subroutine'].__dict__)


    def create_token(self, *token, **kwargs):
        self.create_factory_types()
        # *token allow a compound token
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        token_ = tuple([tmp.upper() for tmp in token])
        return tokens.token_type(self.current_rule or NO_RULE, position, False, token=token_, **kwargs)


    def create_reference(self, value, params=None, **kwargs):
        "node that links to symbol table variable, builtin or function (in 'reference')"
        self.create_factory_types()
        assert value != None
        assert type(value) != str
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.clause_type['reference'](self.current_rule or NO_RULE, position, False, value, params, **kwargs)


    def create_nil(self, **kwargs):
        self.create_factory_types()
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return types.Nil(self.current_rule or NO_RULE, position, False, **kwargs)


    def create_literal(self, value, type, **kwargs):
        self.create_factory_types()
        assert value != None
        assert type != None
        if not types.printable(type) in types.ALLOWED_TYPE_NAMES:
            raise NotImplementedError("type '%s' is not implemented" % types.printable(type))
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.types[type.__name__](self.current_rule or NO_RULE, position, False, value, type, **kwargs)


    def create_sep_list(self, *args, sep=',', **kwargs):
        'create a list of parameters with sep as the element separator'
        self.create_factory_types()
        assert args != None
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.clause_type['sep_list'](self.current_rule or NO_RULE, position, False, *args, **kwargs)


    def create_clause(self, clause, **kwargs):
        self.create_factory_types()
        assert clause != None
        clause = clause.lower()
        if not clause in clauses.ALLOWED_CLAUSES:
            raise NotImplementedError("clause '%s' is not implemented" % clause)
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.clause_type[clause](self.current_rule or NO_RULE, position, False, **kwargs)


    def create_unary_op(self, op, operand, need_parens=False, **kwargs):
        'legacy compatible shortcut'
        self.create_factory_types()
        assert op != None
        assert operand != None
        try:
            return self.create_clause('unary_op', op=op, operand=operand, need_parens=need_parens, **kwargs)
        except TypeMismatch as e:
            node = kwargs.pop('node', self.current_node)
            raise e.set_location(self.parser.context(position=node.position),
                    self.parser.pos_to_linecol(node.position))


    def create_operation(self, op, op1, op2, need_parens=False, **kwargs):
        'legacy compatible shortcut'
        self.create_factory_types()
        assert op != None
        assert op1 != None
        assert op2 != None
        try:
            return self.create_clause('operation', op=op, op1=op1, op2=op2, need_parens=need_parens, **kwargs)
        except TypeMismatch as e:
            node = kwargs.pop('node', self.current_node)
            raise e.set_location(self.parser.context(position=node.position),
                    self.parser.pos_to_linecol(node.position))


    def create_case_op(self, op, op2, need_rparens=False, **kwargs):
        self.create_factory_types()
        assert op != None
        assert op2 != None
        try:
            return self.create_clause('case_op', op=op, op2=op2, need_rparens=need_rparens, **kwargs)
        except TypeMismatch as e:
            node = kwargs.pop('node', self.current_node)
            raise e.set_location(self.parser.context(position=node.position),
                    self.parser.pos_to_linecol(node.position))


    def create_initialisation(self, dimensions, values, type, **kwargs):
        'Processes Dim initialisation expressions.'
        self.create_factory_types()
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.initialisation_type(self.current_rule or NO_RULE, position, False, dimensions=dimensions,
                values=values, type=type, **kwargs)


    def create_range(self, begin, end, **kwargs):
        'Processes range clauses, like "1 to 20".'
        self.create_factory_types()
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.clause_type['range'](self.current_rule or NO_RULE, position, False, begin, end, **kwargs)


    def create_point(self, x, y, step, **kwargs):
        'Processes range clauses, like "1 to 20".'
        self.create_factory_types()
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.clause_type['point'](self.current_rule or NO_RULE, position, False, x, y, step, **kwargs)


    def create_box(self, *points, **kwargs):
        'Processes range clauses, like "1 to 20".'
        self.create_factory_types()
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.clause_type['box'](self.current_rule or NO_RULE, position, False, *points, **kwargs)


    def create_statement(self, tokens, **kwargs):
        self.create_factory_types()
        assert tokens != None
        real_tokens = make_tuple(tokens)
        statement = ' '.join([token.title() for token in real_tokens])
        if not tokens in statements.ALLOWED_STATEMENTS:
            raise NotImplementedError("statement '%s' is not implemented" % statement)
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)

        if tokens in statements.SIMPLE_STATEMENTS:
            return self.statement_type[statement](self.current_rule or NO_RULE, position, False, **kwargs)

        statement_type = self.statement_type.get('_'.join([token.title() for token in real_tokens]),
                self.statement_type['Default'])
        kwargs['tokens'] = make_tuple([token.upper() for token in real_tokens])
        return statement_type(self.current_rule or NO_RULE, position, False, **kwargs)


    def create_attribution(self, lvalue, rvalue, **kwargs):
        self.create_factory_types()
        assert lvalue != None
        assert isinstance(lvalue, self.clause_type['reference'])
        assert rvalue != None
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        kwargs['tokens'] = 'Let'
        return self.statement_type['Default'](self.current_rule or NO_RULE, position, False, params=
                (lvalue, '=', rvalue), arg_sep=' ', **kwargs)


    def create_label(self, identifier, type=statements.INTERNAL, line_number=None, **kwargs):
        'legacy compatible shortcut'
        self.create_factory_types()
        assert identifier != None
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.create_statement('Label', identifier=identifier, type=type, line_number=line_number, **kwargs)


    def create_subroutine(self, code_block, **kwargs):
        self.create_factory_types()
        assert code_block != None
        node = kwargs.pop('node', self.current_node)
        position = kwargs.pop('pos', node.position if node else None)
        return self.subroutine_type(self.current_rule or NO_RULE, position, False, code_block, **kwargs)

