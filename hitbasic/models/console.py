# Console, printables and related models

from io import StringIO

from hitbasic import cfg
from hitbasic.models import Node, CmdNode


class PrintExpr(Node):
    def __str__(self):
        if self.expr:
            return f'{self.expr}'
        else:
            return f'{self.sep}'


class PrintParams(Node):
    def __str__(self):
        buffer = StringIO()

        for expr in self.expressions:
            buffer.write(f'{expr}');

        if self.using:
            buffer.write(f'USING{cfg.arg_spacing}{using.fmt};{cfg.arg_spacing}');
            buffer.write(';'.join(self.using.expressions))

        return buffer.getvalue();


class PrintStmt(CmdNode):
    keyword = 'PRINT'

    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.append(
                f'{self.keyword}{cfg.spacing}%s%s' % (f'{self.fileno};{cfg.spacing}' if self.fileno else '',
                self.params if self.params else ''))
        return append_to


class InputStmt(CmdNode):
    keyword = 'INPUT'
