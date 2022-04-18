# Expressions related models


from hitbasic import cfg
from hitbasic.helpers import string
from hitbasic.models import Node


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
            return "(Not {})".format(self.op_)
        else:
            return "{}".format(self.op_)


class CmpOp(Node):
    def __str__(self):
        if self.opr:
            expr = self.op1

            for i, op2 in enumerate(self.op2):
                opr = self.opr[i]
                expr = f"({expr} {opr} {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


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
            expr = self.op_

            for opr in self.opr:
                expr = f"({opr} {expr})"

            return "({})".format(expr)
        else:
            return "{}".format(self.op_)


class ExpOp(Node):
    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} ^ {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class Expression(Node):
    def __str__(self):
        return "{}".format(self.expr)
