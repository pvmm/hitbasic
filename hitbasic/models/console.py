# Console, printables and related models
import os


class PrintExprs(object):
    def __init__(self, parent, exprs, using):
        self.exprs = exprs
        self.using = using

    def __str__(self):
        val = ""
        for expr in self.exprs:
            val += f"{expr}";
        return val;


class PrintStmt(object):
    def __init__(self, parent, fileno, params):
        self.spacing = os.getenv('HITBASIC_SPACING', ' ')
        self.parent = parent
        self.fileno = fileno.id if fileno else None
        self.params = params.exprs if params else None

    def __str__(self):
        return f"PRINT{self.spacing}%s%s" % (f"{self.fileno};{self.spacing}" if self.fileno else '', self.params)

    def write(self, file):
        pass


class InputStmt(object):
    def __init__(self, parent, args):
        self.parent = parent
        self.args = args

    def write(self, file):
        pass
