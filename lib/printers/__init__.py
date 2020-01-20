class LineMarker:
    """MSX-BASIC line marker"""

    def __init__(self, line_number=None, line_addr=None, new_line=True):
        self.line_addr = line_addr
        self.line_num = line_number
        self.new_line = new_line


    def __len__(self):
        return 0


    def __str__(self):
        return ("\n%i " if self.new_line else "%i ") % self.line_num
