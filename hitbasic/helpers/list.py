'list-related helper functions'


import itertools
from collections.abc import Sequence


def flatten(l: list):
    def gen(l):
        for i in l:
            if isinstance(i, Sequence) and not isinstance(i, (str, bytes)):
                yield from flatten(i)
            else:
                yield i
    return [i for i in gen(l)]


def make_tuple(arg):
    if arg is None:
        arg = ()
    elif isinstance(arg, Sequence):
        arg = tuple(arg)
    try:
        return () + arg
    except TypeError:
        return (arg,)


def interleave(seq, delim):
    'Interleave a sequence with delim inserted between each two elements.'
    return [elem for x in seq for elem in (x, delim)][:-1]
