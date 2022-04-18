# Console, printables and related models


from hitbasic import cfg
from hitbasic.models import Node


class PrintExprs(Node):
    def __str__(self):
        val = ''
        for expr in self.exprs:
            val += f'{expr}';
        return val;


class PrintStmt(Node):
    def __str__(self):
        return f'PRINT{cfg.spacing}%s%s' % (
               f'{self.fileno};{cfg.spacing}' if self.fileno else '',
               self.params if self.params else '')


class InputStmt(Node):
    keyword = 'INPUT'
