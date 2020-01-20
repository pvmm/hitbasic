from nodes import *


class Generator:
    LINE_MAX = 255

    def __init__(self, symbol_table, file, line_start=10, line_inc=10, line_len=255):
        self.symbol_table = symbol_table
        self.file = file
        self.line_start = line_start
        self.line_len = line_len


    def p(self, code):
        if isinstance(code, ForStmt): self.write_for_stmt(code)
        elif isinstance(code, DoCondBlockLoop): self.write_do_stmt(code)
        elif isinstance(code, DoBlockLoopCond): self.write_do_stmt(code)
        elif isinstance(code, SelectStmt): self.write_select_stmt(code)
        elif isinstance(code, IfStmt): self.write_if_stmt(code)
        elif isinstance(code, Function): self.write_function(code)
        elif isinstance(code, Subroutine): self.write_subroutine(code)
        else:
            if code == 'Print': self.write_print_stmt(code)
            elif code == 'Input': self.write_input_stmt(code)
            # elif ...



    def print(self, stream):
        p = lambda *args, **kwargs: print(*args, **kwargs, sep='', end='', file=self.file)
        [p(c) for c in stream]

