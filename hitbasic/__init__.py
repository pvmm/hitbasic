__version__ = 1.0

import os


class cfg:
    spacing = os.getenv('HITBASIC_SPACING', ' ')
    arg_spacing = os.getenv('HITBASIC_ARG_SPACING', '')
    compact = os.getenv('HITBASIC_COMPACT', 'true').upper() == 'TRUE'
    line_start = int(os.getenv('HITBASIC_LINE_START', 10))
    line_inc = int(os.getenv('HITBASIC_LINE_INCREMENT', 10))
    line_length = int(os.getenv('HITBASIC_LINE_INCREMENT', 255))
