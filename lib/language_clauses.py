# support statement elements that work
ALLOWED_CLAUSES = ['dim', 'expression', 'fileno', 'initialisation', 'label', 'operation', 'using']
TYPES = {}


def register(identifier, type_):
    identifier = identifier.lower()
    globals()['TYPES'][identifier] = type_
    globals()[identifier] = type_


def create(identifier, *args, **kwargs):
    return globals()[identifier.lower()](None, 0, False, *args, **kwargs)

