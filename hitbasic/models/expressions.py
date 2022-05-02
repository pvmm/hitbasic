# Expressions related models

from io import StringIO
from collections import OrderedDict
from textx import get_children_of_type

from hitbasic import cfg
from hitbasic import msx
from hitbasic.helpers import debug
from hitbasic.helpers.string import join_all
from hitbasic.models import Node, CmdNode, find_parent_type
from hitbasic.msx.types import get_type_from_id


def find_precedence(expr):
    "precedence value of operation, from 0 to 13"
    if type(expr) == Expression:
        return find_precedence(expr.expr)
    if hasattr(expr, 'opr') and expr.opr:
        return expr.precedence
    if hasattr(expr, 'guarded') and expr.guarded:
        return find_precedence(expr.guarded)
    if type(expr) == _Atom:
        return expr.precedence
    return find_precedence(expr.op1)


def find_terminal(expr):
    'detect if node leads to terminal node and return it, otherwise return None'
    if type(expr) == Expression:
        return find_terminal(expr.expr)
    if type(expr) == ImpOp and expr.op2:
        return None
    if type(expr) == EqvOp and expr.op2:
        return None
    if type(expr) == XorOp and expr.op2:
        return None
    if type(expr) == _OrOp and expr.op2:
        return None
    if type(expr) == AndOp and expr.op2:
        return None
    if type(expr) == NotOp and expr.opr:
        return find_terminal(expr.op1)
    if type(expr) == CmpOp and expr.op2:
        return None
    if type(expr) == AddOp and expr.op2:
        return None
    if type(expr) == IdvOp and expr.op2:
        return None
    if type(expr) == MulOp and expr.op2:
        return None
    if type(expr) == NegOp and expr.opr:
        return find_terminal(expr.op1)
    if type(expr) == _Atom:
        if expr.guarded:
            return find_terminal(expr.guarded)
        if expr.num:
            return expr
        if expr.lvalue:
            return expr
        if expr.quoted:
            return expr
    # Everything else
    return find_terminal(expr.op1)


def is_terminal(expr):
    'detect expression resulting type'
    if type(expr) == Expression:
        return is_terminal(expr.expr)
    if type(expr) == _Atom:
        if expr.guarded:
            return find_type(expr.guarded)
        if expr.num:
            return True
        if expr.lvalue:
            return True
        if expr.quoted:
            return True
    # Everything else
    return is_terminal(expr.op1)


def find_type(expr):
    'detect expression resulting type'
    if type(expr) == Expression:
        return find_type(expr.expr)
    if type(expr) == ImpOp and expr.op2:
        return msx.types.Integer
    if type(expr) == EqvOp and expr.op2:
        return msx.types.Integer
    if type(expr) == XorOp and expr.op2:
        return msx.types.Integer
    if type(expr) == _OrOp and expr.op2:
        return msx.types.Integer
    if type(expr) == AndOp and expr.op2:
        return msx.types.Integer
    if type(expr) == NotOp and expr.opr:
        return msx.types.Integer
    if type(expr) == CmpOp and expr.op2:
        return msx.types.Boolean
    if type(expr) == AddOp and expr.op2:
        return coerce_type(expr.op1, expr.op2)
    if type(expr) == IdvOp and expr.op2:
        return msx.types.Integer
    if type(expr) == MulOp and expr.op2:
        return coerce_type(expr.op1, expr.op2)
    if type(expr) == NegOp and expr.opr:
        return msx.types.Integer
    if type(expr) == _Atom:
        if expr.lvalue:
            # TODO check variable type
            return msx.types.Integer
        if expr.guarded:
            return find_type(expr.guarded)
        if expr.num:
            # TODO check for floating point
            return msx.types.Integer
        if expr.quoted:
            return msx.types.String
    # Onion
    return find_type(expr.op1)


class VarNode(Node):
    def __init__(self, identifier, **kwargs):
        self.identifier = identifier
        super().__init__(**kwargs)


    def __str__(self):
        return self.identifier


class Scalar(VarNode):
    pass


class Array(VarNode):
    def __str__(self):
        return f'{self.identifier}({join_all(self.args)})'


    def processor(self, symbol_table):
        # Find statement this expression belongs to
        stmt = find_parent_type(CmdNode, self)
        assert stmt, "expected statement that contains this expression was not found"

        # Create temporary variable for attribution statement
        type_ = get_type_from_id(self.identifier)
        var = symbol_table.create_hitbasic_var(type_=type_, inner=True)
        mapping = (var, self)

        if hasattr(stmt, '_func_mapping'):
            stmt._func_mapping.append(mapping)
        else:
            stmt._func_mapping = [mapping]

        return var


class Expression(Node):
    #precedence = 14

    def __str__(self):
        if hasattr(self, 'op2') and self.op2:
            buffer = StringIO()
            op1 = self.op1

            if find_precedence(op1) > self.precedence:
                buffer.write(f'({op1})')
            else:
                buffer.write(f'{op1}')

            for opr, op2 in zip(self.opr, self.op2):
                buffer.write(f'{cfg.arg_spacing}{opr}{cfg.arg_spacing}')
    
                if find_precedence(op2) > self.precedence:
                    buffer.write(f'({op2})')
                else:
                    buffer.write(f'{op2}')

            return buffer.getvalue()

        elif hasattr(self, 'opr') and self.opr:
            opr, op1 = self.opr, self.op1
            return f'{opr}{cfg.arg_spacing}{op1}'

        if hasattr(self, 'op1') and self.op1:
            return f'{self.op1}'
        else:
            return f'{self.expr}'


class ImpOp(Expression):
    precedence = 13


class EqvOp(Expression):
    precedence = 12


class XorOp(Expression):
    precedence = 11


class _OrOp(Expression):
    precedence = 10


class AndOp(Expression):
    precedence = 9


class NotOp(Expression):
    precedence = 8


class CmpOp(Expression):
    precedence = 7


class AddOp(Expression):
    precedence = 6


class ModOp(Expression):
    precedence = 5


class IdvOp(Expression):
    precedence = 4


class MulOp(Expression):
    precedence = 3


class NegOp(Expression):
    precedence = 2


class ExpOp(Expression):
    precedence = 1


class _Atom(Expression):
    precedence = 0

    def __str__(self):
        if self.quoted:
            return f'"{self.quoted}"'
        if self.lvalue:
            return f'{self.lvalue}'
        if self.guarded:
            return f'{self.guarded}'
        if self.num:
            return f'{self.num}'
        assert(False)

