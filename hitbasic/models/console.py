# Console, printables and related models

class PrintParams(object):
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
        self.parent = parent
        self.fileno = fileno
        self.params = params

    def __str__(self):
        return "{} {}".format(self.fileno + ";" if self.fileno else "", self.params)

    def write(self, file):
        pass


class InputStmt(object):
    def __init__(self, parent, args):
        self.parent = parent
        self.args = args

    def write(self, file):
        pass
