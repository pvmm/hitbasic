from io import BytesIO
from hitbasic.models import *
from hitbasic.models.label import NUMERIC, PLACEHOLDER
from hitbasic.exceptions import *
from hitbasic import cfg
from hitbasic.symbol_table import SymbolTable


LabelMark = label.LabelMark


class AsciiFileGenerator:
    line_start = cfg.line_start
    line_inc = cfg.line_inc
    line_len = cfg.line_length

    def __init__(self):
        self.symbol_table = SymbolTable()


    def fits_in_line(self, stmt, available_space):
        return len(str(stmt).split("\n")[0]) <= available_space


    def process_stmt(self, available, stmt, line_num, buffer = None):
        if available <= 0:
            if buffer: buffer.write(b"\r\n")
            available = self.line_len
            linemark = f'{line_num} '
            available -= len(linemark)
            if available <= 0:
                raise LineTooShort(stmt = stmt)

            if not self.fits_in_line(stmt, available):
                raise LineTooShort(line_num = line_num)
        else:
            if cfg.compact: available -= 1
            if available <= 0:
                return self.process_stmt(0, stmt, line_num + self.line_inc, buffer)

        if stmt.multiline:
            if not self.fits_in_line(stmt, available):
                # try again on an fresh new line
                return self.process_stmt(0, stmt, line_num + self.line_inc, buffer)

            for text in str(stmt).split("\n"):
                if buffer:
                    buffer.write(bytes(f"{text}\r\n", 'utf-8'))
                line_num += self.line_inc

        elif self.fits_in_line(stmt, available - (1 if self.first_stmt else 0)):
            line = str(stmt) if self.first_stmt else f':{stmt}'
            self.first_stmt = False
            if buffer: buffer.write(bytes(line, 'utf-8'))
            return line_num, available - len(line)

        line_num += self.line_inc
        if buffer: buffer.write(b"\r\n")
        return self.process_stmt(0, stmt, line_num, buffer)


    def process(self, program, line_start = 10):
        buffer = BytesIO()

        self.first_stmt = True
        line_len = self.line_len
        current_label = None
        old_line_num = line_num = line_start
        old_stmt_line_num = 0

        for item in program:
            if type(item) == LabelMark:
                item.line_num = line_num

                if item.type == NUMERIC:
                    if item.line_num < old_stmt_line_num:
                        raise InvalidLineNumber(old_stmt_line_num, item.line_num, item._tx_position)
                    old_stmt_line_num = item.line_num

                self.symbol_table.store_label(item)
                current_label = item
                continue
            else:
                item.label = current_label

            line_num, line_len = self.process_stmt(line_len, item, line_num, buffer)

        return buffer


Generator = AsciiFileGenerator

