
class LineTooShort(Exception):
    def __init__(self, stmt = None, line_num = None):
        if stmt:
            message = 'Default line length is too short to fit %s statement on it' % stmt.__class__
        else:
            message = 'Line is too small to write statement on line %s' %  line_num

        super().__init__(message)


class InvalidLineNumber(Exception):
    def __init__(self, old_line_num, new_line_num, pos):
        message = 'Line number %s smaller than previous line number %s' % (new_line_num, old_line_num)
        super().__init__(message)
