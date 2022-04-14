# Control structures and related models


class IfThenOneLiner(object):
    def __init__(self, parent, expr, statements):
        self.parent = parent
        self.expr = expr
        self.statements = statements

    def write(self, file):
        pass


class IfThenElseOneLiner(object):
    def __init__(self, parent, expr, statements):
        self.parent = parent
        self.expr = expr
        self.statements = statements

    def write(self, file):
        pass


IfThenStmt = IfThenOneLiner


class IfThenElseStmt(IfThenElseOneLiner):
    def __init__(self, parent, expr, thenStmts, elseStmts):
        self.parent = parent
        self.expr = expr
        self.thenStmts = thenStmts
        self.elseStmts = elseStmts


class ForStmt(object):
    def __init__(self, parent, var, range):
        self.parent = parent
        self.var = var
        self.range = range

    def write(self, file):
        pass


class NextStmt(object):
    def __init__(self, parent, vars):
        self.parent = parent
        self.vars = vars

    def write(self, file):
        pass


class SelectStmt(object):
    def __init__(self, parent, expr, cases):
        self.parent = parent
        self.expr = expr
        self.cases = cases

    def write(self, file):
        pass


class DoLoopStmt(object):
    def __init__(self, parent, condition, statements):
        self.parent = parent
        self.condition = condition
        self.statements = statements

    def write(self, file):
        pass


class FuncStmt(object):
    def __init__(self, parent, header, statements):
        self.parent = parent
        self.header = header
        self.statements = statements

    def write(self, file):
        pass
