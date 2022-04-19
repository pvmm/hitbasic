# Control structures and related models


from hitbasic.helpers import string
from hitbasic.models import Node
from hitbasic import cfg


class BranchStmt(Node):
    def __str__(self):
        return f'%s{cfg.spacing}%s' % (self.type.upper(), self.adr)


class IfThenOneLiner(Node):
    keyword = 'IF'

    def __str__(self):
        return f'%s{cfg.spacing}%s THEN' % (self.keyword, self.expr)


class IfThenElseOneLiner(Node):
    keyword = 'IF'


class IfThenStmt(Node):
    keyword = 'IF'


class IfThenElseStmt(Node):
    keyword = 'IF'


class ForStmt(Node):
    keyword = 'FOR'


class NextStmt(Node):
    keyword = 'NEXT'

    def __str__(self):
        return f'NEXT{cfg.spacing}%s' % string.joinAll(self.vars, ',')


class SelectStmt(Node):
    keyword = 'SELECT'


class DoLoopStmt(Node):
    keyword = 'DO'


class FuncStmt(Node):
    keyword = 'FUNCTION'

