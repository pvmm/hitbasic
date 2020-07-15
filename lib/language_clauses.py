# support statement elements that work
ALLOWED_CLAUSES = ['dim', 'expression', 'fileno', 'initialisation', 'label', 'operation', 'unary_op', 'using',
                   'case', 'case_op', 'tuple']
TYPES = {}

# case type
CASE_IS = 0
CASE_ELSE = 1


def register(type_id, type_):
    type_id = type_id.lower()
    globals()['TYPES'][type_id] = type_
    globals()[type_id] = type_


def create(type_id, *args, **kwargs):
    return globals()[type_id.lower()](None, 0, False, *args, **kwargs)
