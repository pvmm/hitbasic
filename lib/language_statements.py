import re

from types import SimpleNamespace
from contextlib import suppress

from . import NO_RULE
from . import language_types as types


# what currently works
ALLOWED_STATEMENTS = [ 'Branch', 'Cls', 'Circle', 'Color', 'Conditional', 'Default', 'Dim', 'Do_Until', 'Do_While',
                       'Draw', 'End', ('Exit', 'Do'), 'For_Loop', 'Goto', 'Gosub', 'Input', 'Label', 'Let', 'Line',
                       'Loop_Until', 'Loop_While', 'Multiple', 'Next', 'Paint', 'Play', 'Preset', 'Print', 'Pset',
                       'Put Sprite', 'Return', 'Screen', 'Select', '?' ]
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


def create_signature(params):
    result = ''
    for p in params:
        if type(p) == types.Integer: result += 'i'
        if type(p) == types.String: result += 's'
    return result
    # ptypes = { types.Integer: 'i', types.String: 's' }
    # return [ptypes[p] for p in params]


class RegExpError(Exception): pass


def create_regexp(pattern):
    'create a pattern for matching against statement invocation'
    ctypes = {'i': 'i', 's': 's', 'a': '(i|s)'}
    params = []
    re_params = []
    count = 0
    in_group = False
    i = iter(pattern)

    with suppress(StopIteration):
        c = next(i)
        while True:
            tmp = ''
            # start a group
            if c == '(':
                tmp += c
                c = next(i)
                in_group = True
            # read parameter type
            while in_group:
                if c in ctypes.keys():
                    count += 1
                    params.append(c)
                    tmp += ctypes[c]
                    c = next(i)
                    # read selector
                    if c == '|':
                        tmp += c
                        c = next(i)
                if c == ')':
                    if len(tmp) and tmp[-1] == '|':
                        raise RegExpError('parameter expected')
                    tmp += c
                    c = next(i)
                    in_group = False
                else:
                    raise RegExpError('unexpected operator %s' % c)
            else:
                if c == ')':
                    raise RegExpError('selector not inside a group')
                if c in ctypes.keys():
                    params.append(c)
                    count += 1
                    tmp += ctypes[c]
                    c = next(i)
            # optional parameter?
            if c == '?':
                if tmp == '':
                    raise RegExpError('parameter missing')
                if len(tmp) and tmp[-1] == '?':
                    raise RegExpError("can't chain optionals")
                tmp += c
                c = next(i)
            re_params.append(tmp)
    # create object
    return SimpleNamespace(pattern='^(?=(%s))(.*)$' % ''.join(re_params),
                           count=lambda: count,
                           type=lambda n: params[n])
