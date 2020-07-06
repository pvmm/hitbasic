import itertools
import io

from collections import Sequence
from contextlib import suppress

from .exceptions import *


#debug = print
debug = lambda *x: None


class p:
    'Use print()-like calls for buffer construction.'

    def __init__(self):
        self.buffer = io.StringIO()


    def reset(self):
        self.buffer = io.StringIO()


    def __call__(self, *args):
        print(*args, sep='', end='', file=self.buffer)


    def getvalue(self):
        return self.buffer.getvalue()


p = p()


def first_node(lst):
    if not isinstance(lst, (tuple, list)):
        return lst
    for item in lst:
        if isinstance(item, list):
            return first_node(item)
        else:
            return item
    return None


def nth_node(lst, n):
    tmp = lst[:] # create array copy
    tmp = flatten(tmp)
    return tmp[n]


def make_tuple(arg):
    if arg is None:
        arg = ()
    elif isinstance(arg, list):
        arg = tuple(arg)
    try:
        return () + arg
    except TypeError:
        return (arg,)


def insert(seq, value, after=(), before=()):
    tmp = []
    for item in seq:
        if item in make_tuple(after):
            tmp.extend([item, value])
        elif item in make_tuple(before):
            tmp.extend([value, item])
        else:
            tmp.append(item)
    return seq.__class__(tmp)


def interleave(seq, delims):
    'Interleave a sequence with delim inserted between each two elements.'
    packet = []
    packet.append(seq)
    delims = make_tuple(delims)

    for delim in delims:
        packet.append(delim * len(seq))

    result = [*itertools.chain(*zip(*packet))][0:-1 * len(delims)]
    return seq.__class__(result)


def flat_str(l: list):
    with suppress(AttributeError):
        return l.flat_str()
    return str().join([i.flat_str() for i in l])


def flatten(l: list):
    def gen(l):
        for i in l:
            if isinstance(i, Sequence) and not isinstance(i, (str, bytes)):
                yield from flatten(i)
            else:
                yield i
    return [i for i in gen(l)]


def search_position(*args):
    for arg in args:
        if hasattr(arg, 'position'):
            return arg.position
    return None


def parse_comma_list(lst, nil_element=None, expect_parenthesis=False, max=None):
    'BASIC ranges might allow empty values and we must account for that.'
    if expect_parenthesis and not (lst[0] == '(' and lst[-1] == ')'):
        raise SyntaxError_('matching parenthesis missing')
    result = []
    expected_item = True
    for item in iter(lst[1:-1] if expect_parenthesis else lst):
        if expected_item and item == ',':
            result.append(nil_element)
            max -= 1
        elif expected_item and item != ',':
            result.append(item)
            expected_item = False
            max -= 1
        elif not expected_item and item != ',':
            raise SyntaxError_('comma expected, not %s' % item)
        elif not expected_item and item == ',':
            expected_item = True
    if expected_item:
        result.append(nil_element)
        max -= 1
    if max < 0:
        raise SyntaxError_('too many values (received %s more)' % (-max))
    return tuple(result)


def parse_arg_list(lst, sep=',', nil_element=None, max=None):
    'implements a list of arguments separated by comma where some elements can be empty, but not the last one.'
    result = []
    s = []
    item = None
    item_type = None
    for item in (it := iter(lst)):
        if item == sep:
            if not s:
                result.append(nil_element)
            else:
                if item_type is str:
                    result.append(''.join(s))
                else:
                    result.extend(s)
                s = []
            if max != None: max -= 1
        elif item != sep:
            item_type = type(item)
            s.append(item)
    if s and item != ',':
        if item_type is str:
            result.append(''.join(s))
        else:
            result.extend(s)
        if max != None: max -= 1
    elif item == ',':
        # Last element cannot be empty
        raise MissingOperand()
    if max < 0:
        raise SyntaxError_('too many values (received %s more)' % (-max))
    return tuple(result)


# Name mangling sufix
TYPE_CHAR = {
        'Boolean': 'b', 'BOOL': 'b',
        'Integer': 'n', 'INT': 'n',
        'String': 's', 'STR': 's',
        'Single': 'n', 'SNG': 'n',
        'Double': 'n', 'DBL': 'n'
}


PRINTABLE_TYPE = {
        'b': 'Boolean', 'BOOL': 'Boolean', 'Boolean': 'Boolean',
        'i': 'Integer', 'INT': 'Integer', 'Integer': 'Integer',
        's': 'String', 'STR': 'String', 'String': 'String',
        'f': 'Single', 'SNG': 'Single', 'Single': 'Single',
        'd': 'Double', 'DBL': 'Double', 'Double': 'Double'
}


def mangle_function(f):
    mangled_name, n = f.name, ''
    #print('f =', f, f.types, type(f))
    for p in f.params:
        #print('p =',p, type(p))
        n += TYPE_CHAR[p.types]
    with suppress(KeyError):
        result = mangled_name + n + ':' + TYPE_CHAR[str(f.types[0])]
        print('result =', result)
        return result
    raise SyntaxError_('unknown type', f.types[0])


def print_parameters(obj):
    return ', '.join([PRINTABLE_TYPE[x.type] for x in obj.params])
