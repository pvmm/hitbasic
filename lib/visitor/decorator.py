import functools


def store_node(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args[0].current_node = args[1]
        args[0].current_rule = args[1].rule
        return func(*args, **kwargs)
        args[0].current_node = None
        args[0].current_rule = None
    return wrapper

