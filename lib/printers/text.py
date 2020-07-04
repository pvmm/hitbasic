class Generator:
    LINE_MAX = 255

    def __init__(self, symbol_table, file, line_start=10, line_inc=10, line_len=255):
        self.symbol_table = symbol_table
        self.file = file
        self.line_start = line_start
        self.line_inc = line_inc
        self.line_len = line_len


    def print(self, stream):
        p = lambda *args, **kwargs: print(*args, **kwargs, sep='', end='\n', file=self.file)
        line_number = self.line_start
        # 1st pass: find label values
        for stmt in stream:
            token, *params = stmt
            if token.startswith('@'):
                self.symbol_table.update_label(token[1:], line_number)
            else:
                line_number += self.line_inc
        # 2nd pass: print with labels replaced with line numbers
        line_number = self.line_start
        for stmt in stream:
            token, *params = stmt
            if token.startswith('@'): continue
            params = list(map(lambda x: self.symbol_table.get_label(x[1:]) if str(x).startswith('@') else x, 
                        filter(lambda x: x != '\n', params)))
            p(line_number, ' ', token, *params)
            line_number += self.line_inc

