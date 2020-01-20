from contextlib import suppress
from arpeggio import Terminal
from math import trunc

from .decorator import *
from ..helper import *

from .. import language_types as types


class ExpressionVisitor:

    def __init__(self, parser):
        self.parser = parser


    def visit_exprs(self, node, children):
        return children


    def visit_expr(self, node, children):
        return children.pop()


    def visit_comp_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            result = self.create_operation(op, op1, op2)
        else:
            result = children.pop()
        return result


    def visit_add_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 + op2 if op == '+' else op1 - op2
            else:
                result = self.create_operation(op, op1, op2)
        else:
            result = children.pop()
        return result


    def visit_mod_op(self, node, children):
        if len(children) == 2:
            op1, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 % op2
            else:
                result = self.create_operation('MOD', op1, op2)
        else:
            result = children.pop()

        return result


    def visit_idiv_op(self, node, children):
        if len(children) == 2:
            op1, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 // op2
            else:
                result = self.create_operation('\\', op1, op2)
        else:
            result = children.pop()

        return result


    def visit_mul_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 * op2 if op == '*' else op1 / op2
            else:
                result = self.create_operation(op, op1, op2)
        else:
            result = children.pop()

        return result


    def visit_neg_op(self, node, children):
        if len(children) > 1:
            signal, operand = children
            if signal == '-':
                if self.pp_flag and operand.is_constexp:
                    operand.value = -operand.value
                    result = operand
                else:
                    result = self.create_unary(signal, operand, node=node)
            else:
                result = operand # +number has obviously no effect
        else:
            result = children.pop()
        return result


    def visit_exp_op(self, node, children):
        if len(children) > 1:
            leftmost = children.pop(0)
            while len(children) > 0:
                op2 = children.pop(0)
                node_begin = leftmost.position
                node_end = op2.position
                if self.pp_flag and leftmost.is_constexp and op2.is_constexp:
                    leftmost = leftmost ** op2
                else:
                    leftmost = self.create_operation('^', leftmost, op2)
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
            result = self.create_operation(op, op1, op2)
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
                result = self.create_operation(op, op1, op2)
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
            result = self.create_operation(op, op1, op2)
        else:
            result = children.pop()
        return result


    def visit_num_add_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 + op2 if op == '+' else op1 - op2
            else:
                result = self.create_operation(op, op1, op2)
        else:
            result = children.pop()
        return result


    def visit_num_mod_op(self, node, children):
        if len(children) == 2:
            op1, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 % op2
            else:
                result = self.create_operation('MOD', op1, op2)
        else:
            result = children.pop()
        return result


    def visit_num_idiv_op(self, node, children):
        if len(children) == 2:
            op1, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 // op2
            else:
                result = self.create_operation('\\', op1, op2)
        else:
            result = children.pop()
        return result


    def visit_num_mul_op(self, node, children):
        if len(children) == 3:
            op1, op, op2 = children
            if self.pp_flag and op1.is_constexp and op2.is_constexp:
                result = op1 * op2 if op == '*' else op1 / op2
            else:
                result = self.create_operation(op, op1, op2)
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
                    result = self.create_unary(signal, operand, node=node)
            else:
                result = operand # +number has obviously no effect
        else:
            result = children.pop()
        return result


    def visit_num_exp_op(self, node, children):
        if len(children) > 1:
            leftmost = children.pop(0)
            while len(children) > 0:
                op2 = children.pop(0)
                node_begin = leftmost.position
                node_end = op2.position
                if self.pp_flag and leftmost.is_constexp and op2.is_constexp:
                    leftmost = leftmost ** op2
                else:
                    leftmost = self.create_operation('^', leftmost, op2)
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

