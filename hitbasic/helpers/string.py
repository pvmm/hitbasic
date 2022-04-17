import functools

from io import StringIO
from hitbasic import spacing, arg_spacing


has_next = lambda items: functools.reduce(lambda total, x: total | bool(x), items, False)

join_all = lambda items, sep: f'{sep}{arg_spacing}'.join([str(item) if type(item) != None else '' for item in items])


def write_list(args = [], sep=','):
    s = StringIO()

    s.write(str(args[0]) if args[0] != None and has_next(args[1:]) else '')

    for i, arg in enumerate(args[1:]):
        s.write(f'{sep}{arg_spacing}%s' % (arg if arg != None and has_next(args[i:]) else ''))

    return s.getvalue()
