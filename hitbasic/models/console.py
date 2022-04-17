# Console, printables and related models


from hitbasic import spacing
from hitbasic.models import Node


class PrintExprs(Node):
    def __str__(self):
        val = ''
        for expr in self.exprs:
            val += f'{expr}';
        return val;


class PrintStmt(Node):
    def __str__(self):
        return f'PRINT{spacing}%s%s' % (
               f'{self.fileno};{spacing}' if self.fileno else '',
               self.params if self.params else '')


class InputStmt(Node):
    keyword = 'INPUT'
