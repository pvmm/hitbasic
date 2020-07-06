import functools


def store_node(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.current_node = args[0]
        self.current_rule = args[0].rule
        return func(self, *args, **kwargs)
        self.current_node = None
        self.current_rule = None
    return wrapper
