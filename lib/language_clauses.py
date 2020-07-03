# support statement elements that work
ALLOWED_CLAUSES = ['dim', 'expression', 'fileno', 'initialisation', 'label', 'operation', 'unary_op', 'using',
                   'case', 'case_op']
TYPES = {}

# case type
CASE_IS = 0
CASE_ELSE = 1


def register(identifier, type_):
    identifier = identifier.lower()
    globals()['TYPES'][identifier] = type_
    globals()[identifier] = type_


def create(identifier, *args, **kwargs):
    return globals()[identifier.lower()](None, 0, False, *args, **kwargs)

