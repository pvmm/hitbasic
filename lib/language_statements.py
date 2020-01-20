from . import NO_RULE


# what currently works
ALLOWED_STATEMENTS = [ 'Branch', 'Cls', 'Circle', 'Color', 'Conditional', 'Default', 'Dim', 'Do_Until', 'Do_While',
                       'Draw', 'End', ('Exit', 'Do'), 'For_Loop', 'Input', 'Label', 'Let', 'Line', 'Loop_Until',
                       'Loop_While', 'Multiple', 'Next', 'Paint', 'Play', 'Preset', 'Print', 'Pset', 'Return',
                       'Screen', '?'  ]
# non-parameterised statements
SIMPLE_STATEMENTS = [ 'Beep', 'Cls', 'End', 'Return', ('Exit', 'Do') ]

GOTO, GOSUB = 'GOTO', 'GOSUB'
BRANCH_TYPE = [ GOTO, GOSUB ]

INTERNAL, BEGIN_PROGRAM, END_PROGRAM = 0, 1, 2
LABEL_TYPE = [ INTERNAL, BEGIN_PROGRAM, END_PROGRAM ]

TYPES = {}


def register(token, type_):
    globals()['TYPES'][token] = type_
    globals()[token] = type_


def create_label(identifier, *args, **kwargs):
    return globals()['Label'](NO_RULE, 0, False, identifier, *args, **kwargs)


def create(token, *args, **kwargs):
    return globals()[token.title()](NO_RULE, 0, False, *args, **kwargs)


class Statement:
    def __init__(self, *tokens):
        self.tokens = tuple([token.upper() for token in tokens])

