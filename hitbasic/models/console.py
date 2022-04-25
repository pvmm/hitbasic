# Console, printables and related models

from io import StringIO

from hitbasic import cfg
from hitbasic.models import Node, CmdNode


class PrintParams(Node):
    def __str__(self):
        val = StringIO()

        for expr in self.exprs:
            val.write(f'{expr}');

        if self.using:
            val.write(f'USING{cfg.arg_spacing}{using.fmt};{cfg.arg_spacing}');
            val.write(';'.join(self.using.exprs))

        return val.getvalue();


class PrintStmt(CmdNode):
    keyword = 'PRINT'

    def __str__(self):
        return f'{self.keyword}{cfg.spacing}%s%s' % (
               f'{self.fileno};{cfg.spacing}' if self.fileno else '',
               self.params if self.params else '')


class InputStmt(CmdNode):
    keyword = 'INPUT'
