import functools

from io import StringIO
from hitbasic import cfg


join_all = lambda items, sep=',': f'{sep}{cfg.arg_spacing}'.join([str(item) if type(item) != None else '' for item in items])

none_list = lambda items: functools.reduce(lambda total, x: total and x == None, items, True)


def write_list(args = [], sep=',', stmt=None):
    s = StringIO()

    if len(args) and args[0] != None:
        s.write(str(args[0]))
    for i, arg in enumerate(args[1:], start=1):
        if none_list(args[i:]): break
        s.write(f'{sep}{cfg.arg_spacing}%s' % (arg if arg != None else ''))

    return s.getvalue()
