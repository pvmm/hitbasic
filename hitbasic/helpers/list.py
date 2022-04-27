'list-related helper functions'


from collections.abc import Sequence


def flatten(l: list):
    def gen(l):
        for i in l:
            if isinstance(i, Sequence) and not isinstance(i, (str, bytes)):
                yield from flatten(i)
            else:
                yield i
    return [i for i in gen(l)]
