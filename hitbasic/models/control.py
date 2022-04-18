# Control structures and related models


from hitbasic.helpers import string
from hitbasic.models import Node
from hitbasic import spacing


class BranchStmt(Node):
    def __str__(self):
        return f'%s{spacing}%s' % (self.type.upper(), self.adr)


class IfThenOneLiner(Node):
    keyword = 'IF'


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
        print(f'NEXT{spacing}%s' % string.joinAll(self.vars, ','))


class SelectStmt(Node):
    keyword = 'SELECT'


class DoLoopStmt(Node):
    keyword = 'DO'


class FuncStmt(Node):
    keyword = 'FUNCTION'

