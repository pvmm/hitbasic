import functools

from io import StringIO
from hitbasic import spacing


has_next = lambda items: functools.reduce(lambda total, x: total | bool(x), items, False)

join_all = lambda items, sep: f'{sep}{spacing}'.join([str(item) if type(item) != None else '' for item in items])


def write_list(args = [], sep=','):
    s = StringIO()

    for i, arg in enumerate(args):
        s.write(f'{sep}{spacing}%s' % (arg if arg != None and has_next(args[i:]) else ''))

    return s.getvalue()
