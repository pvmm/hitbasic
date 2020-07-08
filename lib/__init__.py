from contextlib import suppress


class NO_RULE: rule_name = '<no rule>'


def subc(module, cls_name):
    'remove unnecessary bits of a module class and turn it into a dictionary for type composition'
    subcls = dict(module.__dict__[cls_name].__dict__)
    remove = ['__module__', '__dict__', '__weakref__', '__doc__' ]
    for r in remove:
        with suppress(KeyError):
            del subcls[r]
    return subcls
