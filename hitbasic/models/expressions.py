# Expressions related models


from hitbasic import cfg
from hitbasic import msx
from hitbasic.helpers import debug, string
from hitbasic.models import Node


def find_terminal(expr):
    'detect if node leads to terminal node and return it, otherwise return None'
    if type(expr) == NumericExp:
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
    if type(expr) == _Atom and expr.expr:
        return find_terminal(expr.expr)
    if type(expr) == _Atom and expr.num:
        return expr
    if type(expr) == _Atom and expr.lvalue:
        return expr

    if type(expr) == StringExp:
        if expr.concat:
            return None
        if expr.opr:
            return None
        return expr

    return find_terminal(expr.op1)


def is_terminal(expr):
    'detect expression resulting type'
    if type(expr) == NumericExp:
        return is_terminal(expr.expr)
    if type(expr) == _Atom and expr.expr:
        return find_type(expr.expr)
    if type(expr) == _Atom and expr.num:
        return True
    if type(expr) == _Atom and expr.lvalue:
        return True

    if type(expr) == StringExp:
        if expr.concat:
            return False
        if expr.opr:
            return False
        return True

    return is_terminal(expr.op1)

def find_type(expr):
    'detect expression resulting type'
    if type(expr) == NumericExp:
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
    if type(expr) == _Atom and expr.expr:
        return find_type(expr.expr)
    if type(expr) == _Atom and expr.num:
        return msx.types.Integer
    if type(expr) == _Atom and expr.lvalue:
        return msx.types.Integer


    if type(expr) == StringExp:
        if expr.concat:
            return msx.types.String
        if expr.opr:
            return msx.types.Boolean
        return msx.types.String

    return find_type(expr.op1)


class Scalar(Node):
    def __str__(self):
        return self.identifier


class StringExp(Node): pass


class NumericExp(Node):
    def __str__(self):
        return f'{self.expr}'


class Array(Node):
    def __str__(self):
        print('sb=', self.subscripts)
        return f'{self.identifier}({string.joinAll(self.subscripts)})'


class ImpOp(Node):
    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Imp {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class EqvOp(Node):
    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Eqv {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class XorOp(Node):
    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Xor {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class _OrOp(Node):
    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Or {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class AndOp(Node):
    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} And {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class NotOp(Node):
    def __str__(self):
        if self.opr:
            return "(Not {})".format(self.op1)
        else:
            return "{}".format(self.op1)


class CmpOp(Node):
    def __str__(self):
        if self.opr:
            expr = self.op1
            return f'({expr} {self.opr} {self.op2})'
        else:
            return f'{self.op1}'


class AddOp(Node):
    def __str__(self):
        if self.opr:
            expr = self.op1

            for i, op2 in enumerate(self.op2):
                opr = self.opr[i]
                expr = f"({expr} {opr} {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class ModOp(Node):
    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Mod {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class IdvOp(Node):
    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = rf"({expr} \ {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class MulOp(Node):
    def __str__(self):
        if self.opr:
            expr = self.op1

            for i, op2 in enumerate(self.op2):
                opr = self.opr[i]
                expr = f"({expr} {opr} {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class NegOp(Node):
    def __str__(self):
        if self.opr:
            expr = self.op1

            for opr in self.opr:
                expr = f"({opr} {expr})"

            return f"({self.expr})"
        else:
            return f"{self.op1}"


class ExpOp(Node):
    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} ^ {op2})";

            return f"{self.expr}"
        else:
            assert(self.op1 != None)
            return f"{self.op1}"


class _Atom(Node):
    def __str__(self):
        if not self.num is None:
            return f'{self.num}'
        if not self.lvalue is None:
            return f'{self.lvalue}'
        return '???'


class Expression(Node):
    def __str__(self):
        return f'{self.expr}'
