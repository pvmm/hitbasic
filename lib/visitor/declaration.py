from arpeggio import Terminal

from .decorator import *
from ..helper import *
from ..exceptions import *

from .. import language_tokens as tokens
from .. import language_types as types


def check_init_type(arg, old_type=None):
    if isinstance(arg, list):
        for item in arg:
            if isinstance(item, list):
                new_type = check_init_type(item, old_type)
            elif not old_type:
                new_type = check_init_type(item, old_type)
            else:
                new_type = check_init_type(item, old_type)
            if new_type and old_type and new_type != old_type:
                raise TypeMismatch(types.printable(old_type), types.printable(new_type))
            old_type = new_type
        return old_type
    else:
        if old_type:
            if types.compatible_types(old_type, arg.type):
                return old_type
            raise TypeMismatch(types.printable(old_type), types.printable_type(arg))
        return arg.type


def check_dim(lst, depth=0, stack={}):
    'Find dimensions by iterating over initialization.'
    try:
        if isinstance(lst, list):
            if not stack.get(depth, None):
                stack[depth] = -1
            if len(lst) > stack[depth]:
                stack[depth] = len(lst)
            for x in lst:
                with suppress(TypeError):
                    check_dim(x, depth=depth+1, stack=stack)
        if not depth:
            return tuple(stack.values())
    except TypeError:
        return None # dimensionless


class DeclarationVisitor:
    "Manage a variable's lifecycle"

    def __init__(self):
        self.ANY_RANGE = self.create_range('*', '*')


    def compare_ranges(self, a, b):
        if ((a, b) == (None, None)): return True
        elif a is None or b is None: return False
        elif len(a) != len(b): return False
        for r in zip(a, b):
            if self.ANY_RANGE in r: continue
            if r[0] != r[1]: return False
        return True


    def parse_range(self, lst, expect_parenthesis=True):
        'BASIC ranges might allow empty values and we must account for that.'
        if expect_parenthesis and not (lst[0] == '(' and lst[-1] == ')'):
            raise self.create_exception(SyntaxError_, 'matching parenthesis missing')
        result = []
        expected_item = True
        for item in iter(lst[1:-1] if expect_parenthesis else lst):
            if expected_item and item == ',':
                result.append(self.create_range('*', '*'))
            elif expected_item and item != ',':
                if isinstance(item, Terminal):
                    item = int(item.flat_str())
                    result.append(self.create_range(0, item))
                else:
                    result.append(item)
                expected_item = False
            elif not expected_item and item != ',':
                raise SyntaxError_('comma expected, not %s' % item)
            elif not expected_item and item == ',':
                expected_item = True
        if expected_item:
            result.append(self.create_range('*', '*'))
        return tuple(result)


    @store_node
    def visit_dim_stmt(self, node, children):
        [[*dim_node]] = children
        clauses = []
        code_block = []
        for clause, init in dim_node:
            if not init:
                clauses.append(clause)
            else:
                clauses.append(clause)
                code_block.append(self.create_statement('Dim', clauses=clauses))
                clauses = []
                code_block.extend(init)
        if clauses:
            code_block.append(self.create_statement('Dim', clauses=clauses))
        return self.create_statement('Multiple', code_block=code_block)


    def visit_dim_vars(self, node, children):
        return children


    def write_dim_init(self, var, init_values):
        d = init_values.dimensions
        v = init_values.values
        code_block = []

        if not d:
            ref = self.create_reference(var, node=first_node(init_values))
            code_block.append(self.visit_attr_stmt(ref, [ref, v]))
        elif len(d) == 1:
            for col in range(0, d[0]):
                try:
                    ref = self.create_reference(var, params=(col), node=first_node(init_values))
                    code_block.append(self.visit_attr_stmt(ref, [ref, v[col]]))
                except TypeError:
                    raise self.create_exception(DimInitAccessError, var.reference[:-2], col)
                except IndexError:
                    break # allow partial initialisations
        elif len(d) == 2:
            for row in range(0, d[0]):
                for col in range(0, d[1]):
                    try:
                        ref = self.create_reference(var, params=(row, col), node=first_node(init_values))
                        code_block.append(self.visit_attr_stmt(ref, [ref, v[row][col]]))
                    except TypeError:
                        raise self.create_exception(DimInitAccessError, var.reference[:-2], row, col)
                    except IndexError:
                        break # allow partial initialisations
        elif len(d) == 3:
            for layer in range(0, d[0]):
                for row in range(0, d[1]):
                    for col in range(0, d[2]):
                        try:
                            ref = self.create_reference(var, params=(layer, row, col), node=first_node(init_values))
                            code_block.append(self.visit_attr_stmt(ref, [ref, v[layer][row][col]]))
                        except TypeError:
                            raise self.create_exception(DimInitAccessError, var.reference[:-2], layer, row, col)
                        except IndexError:
                            break # allow partial initialisations
        return code_block


    @store_node
    def visit_dim_var_decl(self, node, children):
        [(identifier, [*ranges]), *init] = children
        if len(init) > 1:
            if tokens.Token('=') in init:
                eq_sn_pos = init.index(tokens.Token('='))
                init_values = init[eq_sn_pos + 1]
                try:
                    init_type = check_init_type(init_values)
                except TypeMismatch as e:
                    raise e.put_location(first_node(init_values))
                dimensions = check_dim(init_values, stack={})
                init_ranges = [self.create_range(0, x-1) for x in dimensions]
                dim_init = self.create_initialisation(dimensions, init_values, init_type, node=
                        first_node(init_values))
            else:
                init_values = None
                dim_init = None
                dimensions = ()
                init_type = types.Any
                init_ranges = None
            if tokens.Token('As') in init:
                as_kw_pos = init.index(tokens.Token('As'))
                type_ = init[as_kw_pos + 1]
            else:
                type_ = types.Any
            try:
                init_values and type_ and types.check_initialisation(type_, init_values)
            except TypeMismatch as e:
                raise self.put_location(e, pos=node[-1].position)
            if init_values:
                # TODO: change the use of compare_ranges to allow partial initializations?
                if self.compare_ranges(ranges, init_ranges) != True:
                    raise self.create_exception(DimRangesMismatch, identifier)
                else:
                    # we prefeer precise ranges.
                    ranges = init_ranges
            try:
                type_ = types.calculate_type(type_, init_type)
            except TypeMismatch as e:
                raise self.put_location(e)
            var = self.symbol_table.create_hitbasic_var(identifier, ranges, type_)
            if dim_init:
                init_code = self.write_dim_init(var, dim_init)
            else:
                init_code = ()
            return self.create_clause('dim', var=var), init_code
        else:
            var = self.symbol_table.create_hitbasic_var(identifier, ranges)
            return self.create_clause('dim', var=var), ()


    def visit_dim_var_type(self, node, children):
        return types.get_type_from_type_id(children.pop())


    def visit_dim_var(self, node, children):
        identifier, *ranges = children
        if ranges: ranges = self.parse_range(flatten(ranges), True)
        return identifier, ranges


    def visit_dim_var_ranges(self, node, children):
        return tuple(children)


    @store_node
    def visit_dim_var_expr(self, node, children):
        if len(children) == 2:
            begin, end = children
        else:
            begin, end = 0, *children
        return self.create_range(begin, end)


    def visit_dim_init(self, node, children):
        if not len(children) and node.flat_str() == '{}':
            return []
        return children.pop()


    def visit_dim_init_array(self, node, children):
        return children


    def visit_dim_var_name(self, node, children):
        return node.flat_str()


    @store_node
    def visit_dim_as_kw(self, node, children):
        return self.create_token(node.flat_str(), node=node)


    @store_node
    def visit_dim_eq_tk(self, node, children):
        return self.create_token(node.flat_str(), node=node)
