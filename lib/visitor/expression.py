from contextlib import suppress
from arpeggio import Terminal
from math import trunc

from .decorator import *
from ..helper import *

from .. import msx
from .. import language_types as types
from .. import language_clauses as clauses


class ExpressionVisitor:

    def __init__(self, parser):
        self.parser = parser


    def visit_exprs(self, node, children):
        return children


    def visit_expr_dasdas(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if op.title() == 'Imp': return self.visit_imp_op(node, children)
            if op.title() == 'Eqv': return self.visit_eqv_op(node, children)
            raise SyntaxError()
        return children


    def visit_expr(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = not(op1) or op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()
        return result


    def visit_eqv_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = (op1 and op2) or (not(op1) and not(op2))
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()
        return result


    def visit_xor_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 ^ op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()
        return result


    def visit_or_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 or op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()
        return result


    def visit_and_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 and op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()
        return result


    def visit_not_op(self, node, children):
        if len(children) == 2:
            op, operand = children
            if self.pp_flag and operand.is_constexp:
                operand.value = not(operand.value)
                result = operand
            else:
                need_parens = False
                if isinstance(operand, (clauses.operation, clauses.unary_op)):
                    #print('operand: %s' % operand.translate())
                    need_parens = msx.OP_PRIORITY[operand.op] < msx.OP_PRIORITY['S']
                result = self.create_unary_op(op, operand, need_parens=need_parens)
        else:
            result = children.pop()
        return result


    def visit_comp_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            need_lparens, need_rparens = False, False
            if isinstance(op1, (clauses.operation, clauses.unary_op)):
                #print('op1: %s' % op1.translate())
                need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
            if isinstance(op2, (clauses.operation, clauses.unary_op)):
                #print('op2: %s' % op2.translate())
                need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
            result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                        node=node[1])
        else:
            result = children.pop()
        return result


    def visit_add_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 + op2 if op == '+' else op1 - op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()
        return result


    def visit_mod_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 % op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()

        return result


    def visit_idiv_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 // op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_parens=need_parens, node=node[1])
        else:
            result = children.pop()

        return result


    def visit_mul_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 * op2 if op == '*' else op1 / op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()

        return result


    def visit_neg_op(self, node, children):
        if len(children) == 2:
            signal, operand = children
            if signal == '-':
                if self.pp_flag and operand.is_constexp:
                    operand.value = -operand.value
                    result = operand
                else:
                    need_parens = False
                    if isinstance(operand, (clauses.operation, clauses.unary_op)):
                        #print('operand: %s' % operand.translate())
                        need_parens = msx.OP_PRIORITY[operand.op] < msx.OP_PRIORITY['S']
                    result = self.create_unary_op(signal, operand, need_parens=need_parens)
            else:
                result = operand # +number has obviously no effect
        else:
            result = children.pop()
        return result


    def visit_exp_op(self, node, children):
        if len(children) > 1:
            op = '^'
            children = list(filter(lambda op: op != '^', children))
            leftmost = children.pop(0)
            while len(children) > 0:
                op2 = children.pop(0)
                node_begin = leftmost.position
                node_end = op2.position
                if self.pp_flag and leftmost.is_constexp and op2.is_constexp:
                    leftmost = leftmost ** op2
                else:
                    need_lparens, need_rparens = False, False
                    if isinstance(leftmost, (clauses.operation, clauses.unary_op)):
                        need_lparens = msx.OP_PRIORITY[leftmost.op] < msx.OP_PRIORITY[op]
                    if isinstance(op2, (clauses.operation, clauses.unary_op)):
                        need_rparens = msx.OP_PRIORITY[op2.op] <= msx.OP_PRIORITY[op] # left association is the default
                    leftmost = self.create_operation(op, leftmost, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                                node=node[1])
            result = leftmost
        else:
            result = children.pop()
        return result


    def visit_optor(self, node, children):
        [optor] = children
        return optor


    def visit_str_expr(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            result = self.create_operation(op, op1, op2, node=node[1])
        else:
            result = children.pop()
        return result


    #def visit_str_comp_op(self, node, children):
    #    if len(children) == 3:
    #        op1, op, op2 = children
    #        result = self.create_operation(op, op1, op2)
    #    else:
    #        result = children.pop()
    #    return result


    def visit_str_add_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 + op2
            else:
                result = self.create_operation(op, op1, op2, node=node[1])
        else:
            result = children.pop()
        return result


    def visit_str_optor(self, node, children):
        [optor] = children
        return optor


    def visit_num_expr(self, node, children):
        return children.pop()


    def visit_num_comp_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            need_lparens, need_rparens = False, False
            if isinstance(op1, (clauses.operation, clauses.unary_op)):
                #print('op1: %s' % op1.translate())
                need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
            if isinstance(op2, (clauses.operation, clauses.unary_op)):
                #print('op2: %s' % op2.translate())
                need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
            result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                        node=node[1])
        else:
            result = children.pop()
        return result


    def visit_num_add_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 + op2 if op == '+' else op1 - op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()
        return result


    def visit_num_mod_op(self, node, children):
        if len(children) == 2:
            op1, op2, op = *children, 'MOD'
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 % op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()

        return result


    def visit_num_idiv_op(self, node, children):
        if len(children) == 2:
            op1, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 // op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation('\\', op1, op2, need_parens=need_parens, node=node[1])
        else:
            result = children.pop()

        return result


    def visit_num_mul_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 * op2 if op == '*' else op1 / op2
            else:
                need_lparens, need_rparens = False, False
                if isinstance(op1, (clauses.operation, clauses.unary_op)):
                    #print('op1: %s' % op1.translate())
                    need_lparens = msx.OP_PRIORITY[op1.op] < msx.OP_PRIORITY[op]
                if isinstance(op2, (clauses.operation, clauses.unary_op)):
                    #print('op2: %s' % op2.translate())
                    need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                result = self.create_operation(op, op1, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                            node=node[1])
        else:
            result = children.pop()

        return result


    def visit_num_neg_op(self, node, children):
        if len(children) > 1:
            signal, operand = children
            if signal == '-':
                if self.pp_flag and operand.is_constexp:
                    operand.value = -operand.value
                    result = operand
                else:
                    need_parens = False
                    if isinstance(operand, (clauses.operation, clauses.unary_op)):
                        #print('operand: %s' % operand.translate())
                        need_parens = msx.OP_PRIORITY[operand.op] < msx.OP_PRIORITY['S']
                    result = self.create_unary_op(signal, operand, need_parens=need_parens)
            else:
                result = operand # +number has obviously no effect
        else:
            result = children.pop()
        return result


    def visit_num_exp_op(self, node, children):
        if len(children) > 1:
            op, leftmost = '^', children.pop(0)
            while len(children) > 0:
                op2 = children.pop(0)
                node_begin = leftmost.position
                node_end = op2.position
                if self.pp_flag and leftmost.is_constexp and op2.is_constexp:
                    leftmost = leftmost ** op2
                else:
                    need_lparens, need_rparens = False, False
                    if isinstance(leftmost, (clauses.operation, clauses.unary_op)):
                        need_lparens = msx.OP_PRIORITY[leftmost.op] < msx.OP_PRIORITY[op]
                    if isinstance(op2, (clauses.operation, clauses.unary_op)):
                        need_rparens = msx.OP_PRIORITY[op2.op] < msx.OP_PRIORITY[op]
                    leftmost = self.create_operation(op, leftmost, op2, need_lparens=need_lparens, need_rparens=need_rparens,
                                node=node[1])
            result = leftmost
        else:
            result = children.pop()
        return result


    def visit_num_optor(self, node, children):
        [optor] = children
        return optor


    @store_node
    def visit_string(self, node, children):
        return self.create_literal(''.join(children), types.String)


    def visit_number(self, node, children):
        return children[0]


    @store_node
    def visit_integer(self, node, children):
        s = ''
        for n in node:
            s += n.flat_str()
        return self.create_literal(int(s), types.Integer)


    def visit_Digit(self, node, children):
        return node

