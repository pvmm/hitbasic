import sys
from io import BytesIO

from hitbasic.models import *
from hitbasic.models import MetaNode
from hitbasic.models.labels import NUMERIC, PLACEHOLDER
from hitbasic.models.meta import EOL
from hitbasic.exceptions import *
from hitbasic import cfg
from hitbasic.symbol_table import SymbolTable


LabelMark = labels.LabelMark


class AsciiFileGenerator:
    line_start = cfg.line_start
    line_inc = cfg.line_inc
    max_len = cfg.line_length

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.buffer = BytesIO()
        self.sep = ''


    def fits_inline(self, stmt, available_space):
        try:
            printables = list(filter(lambda stmt: stmt != None, stmt.printables()))
            print(f'{printables}')
            return len(printables) <= available_space
        except TypeError as e:
            print(f'** {stmt!r} returned invalid printable **', file=sys.stderr)
            raise e


    def process_stmt(self, stmt, first_stmt, line_len, line_num, sep):
        nl = '\n' if self.buffer.getvalue() else ''
        it = iter(stmt.printables())
        s = next(it)

        while True:
            # Extend this to MetaNode
            if isinstance(stmt, EOL):
                first_stmt = True
                line_len = 0
                line_num += self.line_inc
                break

            print(repr(stmt))
            line = f'{nl}{line_num} {s}' if first_stmt else f'{s}'
            llen = len(line) - 1 if nl else 0

            if llen < self.max_len:
                self.buffer.write(bytes(line, 'utf-8'))
                first_stmt = False
                try:
                    s = next(it)
                except(StopIteration):
                    break
            else:
                line_len = 0
                line_num += self.line_inc
                first_stmt = True
                sep = ' '
                nl = '\n'
            sep = stmt.sep

        return first_stmt, line_len, line_num, sep


    def process(self, program, first_stmt = True, line_len = 0, line_start = 10, curr_label = None):
        line_num = line_start
        prev_line_num = 0
        sep = ' '

        for item in program:
            if type(item) == LabelMark:
                item.line_num = line_num
                sep = ' '

                if item.type == NUMERIC:
                    if item.line_num < prev_line_num:
                        raise InvalidLineNumber(prev_line_num, item.line_num, item.get_linecol())
                    prev_line_num = line_num

                self.symbol_table.store_label(item)
                curr_label = item
                continue
            else:
                item.label = curr_label

            first_stmt, line_len, line_num, sep = self.process_stmt(item, first_stmt, line_len, line_num, sep)

        return self.buffer

Generator = AsciiFileGenerator

