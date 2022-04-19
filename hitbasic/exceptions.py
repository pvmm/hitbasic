
class LineTooShort(Exception):
    def __init__(self, stmt = None, line_num = None):
        if stmt:
            message = 'Default line length is too short to fit %s statement on it' % stmt.__class__
        else:
            message = 'Line is too small to write statement on line %s' %  line_num

        super().__init__(message)
