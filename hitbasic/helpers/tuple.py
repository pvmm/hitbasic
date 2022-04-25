
def make_tuple(arg):
    if arg is None:
        arg = ()
    elif isinstance(arg, list):
        arg = tuple(arg)
    try:
        return () + arg
    except TypeError:
        return (arg,)

