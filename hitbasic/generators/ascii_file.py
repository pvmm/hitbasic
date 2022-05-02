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


    def process_stmt(self, stmt, first_stmt, line_len, line_num):
        it = iter(stmt.printables())
        s = next(it)
        nl = ''

        while True:
            # Extend this to MetaNode
            if s == '\n':
                first_stmt = True
                line_len = 0
                line_num += self.line_inc
                try:
                    s = next(it)
                except StopIteration:
                    # Finished
                    break
                continue

            line = f'{nl}{line_num} {s}' if first_stmt else s
            llen = len(line) - (2 if nl else 0)

            if llen < self.max_len:
                self.buffer.write(bytes(line, 'utf-8'))
                first_stmt = False
                try:
                    s = next(it)
                except StopIteration:
                    # Finished
                    break
            else:
                line_len = 0
                line_num += self.line_inc
                first_stmt = True
                nl = '\r\n'

        return first_stmt, line_len, line_num


    def process(self, program, line_start = 10, curr_label = None):
        first_stmt = True
        line_len = 0
        line_num = line_start

        self.process_stmt(program, first_stmt, line_len, line_num)

        return self.buffer

Generator = AsciiFileGenerator

