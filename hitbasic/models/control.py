# Control structures and related models


from hitbasic.helpers import string
from hitbasic.models import Node, CmdNode
from hitbasic import cfg


class BranchStmt(Node):
    def __str__(self):
        return f'%s{cfg.spacing}%s' % (self.stmt.upper(), self.param)


class ForStmt(Node):
    keyword = 'FOR'


class NextStmt(Node):
    keyword = 'NEXT'

    def __str__(self):
        return f'NEXT{cfg.spacing}%s' % string.joinAll(self.vars, ',')


class DoLoopStmt(Node):
    keyword = 'DO'
