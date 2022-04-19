from io import BytesIO
from hitbasic.models import *
from hitbasic.models.label import NUMERIC, PLACEHOLDER
from hitbasic.exceptions import *
from hitbasic import cfg
from hitbasic.symbol_table import SymbolTable


LabelMark = label.LabelMark


class Generator:
    line_start = cfg.line_start
    line_inc = cfg.line_inc
    line_len = cfg.line_length

    def __init__(self):
        self.symbol_table = SymbolTable()


    def process_stmt(self, available, stmt, line_num, buffer = None):
        if available == 0:
            if buffer:
                buffer.write(b"\r\n")
            available = self.line_len
            linemark = f'{line_num} '
            available -= len(linemark)
            if available <= 0:
                raise LineTooShort(stmt = stmt)
            if not stmt.fits(available):
                raise LineTooShort(line_num = line_num)
        else:
            available -= 1 if cfg.compact else 3
            if available < 0:
                return self.process_stmt(0, stmt, line_num + self.line_inc, buffer)

        if stmt.multiline:
            if not stmt.fits(available):
                # try again on an fresh new line
                return self.process_stmt(0, stmt, line_num + self.line_inc, buffer)

            for pos, text in stmt.gen_line(available):
                if buffer:
                    buffer.write(text)
                    buffer.write("\r\n")
                line_num += self.line_inc
        elif stmt.fits(available):
            line = bytes(stmt)
            if buffer: buffer.write(line)
            return line_num + self.line_inc, len(line)


    def process(self, program, line_start = 10):
        buffer = BytesIO()
        current_label = None
        old_line_num = line_num = line_start
        old_stmt_line_num = 0

        for item in program:
            if type(item) == LabelMark:
                item.line_num = line_num

                if item.type == NUMERIC:
                    if item.line_num <= old_stmt_line_num:
                        raise InvalidLineNumber(item, item._tx_position)
                    old_stmt_line_num = item.line_num

                self.symbol_table.store_label(item)
                current_label = item
                continue
            else:
                item.label = current_label

            self.process_stmt(0, item, line_num, buffer)
