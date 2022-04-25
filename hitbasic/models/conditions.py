# Control structures and related models


from hitbasic.models import CmdNode


class IfThenOneLiner(CmdNode):
    keyword = 'IF'


class IfThenElseOneLiner(CmdNode):
    keyword = 'IF'


class IfThenStmt(CmdNode):
    keyword = 'IF'
    def __init__(self, expr, statements):
        self.expr = expr
        self.statements = statements


class IfThenElseStmt(CmdNode):
    keyword = 'IF'
