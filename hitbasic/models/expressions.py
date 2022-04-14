# Expressions related models

class ImpOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Imp {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class EqvOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Eqv {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class XorOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Xor {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class _OrOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Or {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class AndOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} And {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class NotOp(object):
    def __init__(self, parent, opr, op_):
        self.parent = parent
        self.opr = opr
        self.op_ = op_

    def __str__(self):
        if self.opr:
            return "(Not {})".format(self.op_)
        else:
            return "{}".format(self.op_)


class CmpOp(object):
    def __init__(self, parent, op1, opr=None, op2=None):
        self.parent = parent
        self.op1 = op1
        self.opr = opr
        self.op2 = op2

    def __str__(self):
        if self.opr:
            expr = self.op1

            for i, op2 in enumerate(self.op2):
                opr = self.opr[i]
                expr = f"({expr} {opr} {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class AddOp(object):
    def __init__(self, parent, op1, opr=None, op2=None):
        self.parent = parent
        self.op1 = op1
        self.opr = opr
        self.op2 = op2

    def __str__(self):
        if self.opr:
            expr = self.op1

            for i, op2 in enumerate(self.op2):
                opr = self.opr[i]
                expr = f"({expr} {opr} {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class ModOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Mod {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class IdvOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = rf"({expr} \ {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class MulOp(object):
    def __init__(self, parent, op1, opr=None, op2=None):
        self.parent = parent
        self.op1 = op1
        self.opr = opr
        self.op2 = op2

    def __str__(self):
        if self.opr:
            expr = self.op1

            for i, op2 in enumerate(self.op2):
                opr = self.opr[i]
                expr = f"({expr} {opr} {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class NegOp(object):
    def __init__(self, parent, opr, op_):
        self.parent = parent
        self.opr = opr
        self.op_ = op_

    def __str__(self):
        if self.opr:
            expr = self.op_

            for opr in self.opr:
                expr = f"({opr} {expr})"

            return "({})".format(expr)
        else:
            return "{}".format(self.op_)


class ExpOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} ^ {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class Expression(object):
    def __init__(self, parent, expr):
        self.parent = parent
        self.expr = expr

    def __str__(self):
        return "{}".format(self.expr)
