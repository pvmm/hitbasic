# Control structures and related models


from hitbasic.helpers import string
from hitbasic.models import Node
from hitbasic import spacing


class IfThenOneLiner(Node):
    def write(self, file):
        pass


class IfThenElseOneLiner(Node):
    def write(self, file):
        pass


class IfThenStmt(Node):
    pass


class IfThenElseStmt(Node):
    def write(self, file):
        pass


class ForStmt(Node):
    def write(self, file):
        pass


class NextStmt(Node):
    def __str__(self):
        print(f'NEXT{spacing}%s' % string.joinAll(self.vars, ','))

    def write(self, file):
        pass


class SelectStmt(Node):
    def write(self, file):
        pass


class DoLoopStmt(Node):
    def write(self, file):
        pass


class FuncStmt(Node):
    def write(self, file):
        pass
