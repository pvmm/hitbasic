# Control structures and related models


from hitbasic.helpers import string
from hitbasic.models import Node
from hitbasic import cfg


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
