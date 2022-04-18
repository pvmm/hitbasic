from io import BytesIO
from hitbasic.models import *;
from hitbasic import cfg


class Generator:
    line_start = cfg.line_start
    line_inc = cfg.line_inc
    line_len = cfg.line_length

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table


    def process_stmt(self, available, stmt, line_num, buffer = None):
        if available == 0:
            if buffer:
                buffer.write("\r\n")
            available = self.line_len
            linemark = f'{line} '
            available -= len(linemark)
            if available < self.line_len:
                raise LineTooSmall(line = line_num)
            if not stmt.fits(available):
                raise LineTooSmall(stmt = stmt)
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
            line = stmt.line()
            if buffer: buffer.write(line)
            return line_num + self.line_inc, len(line)


    def process(self, statements, line_start = 10):
        buffer = BytesIO()
        current_label = None
        old_line_num = line_num = line_start

        for stmt in statements:

            if type(stmt) == LabelMark:
                if stmt.type == PLACEHOLDER:
                    stmt.line = line_num

                if stmt.type == NUMERIC:
                    if stmt.line < old_line_num:
                        raise InvalidLineNumber(stmt, stmt._tx_position)

                self.symbol_table.add_label(stmt, line_num)
                current_label = stmt
                continue
            else:
                stmt.label = current_label

            process_stmt(0, stmt, line_num, buffer)

