from arpeggio import SemanticError


class VisitorException(Exception):
    'exception thrown inside a visitor'
    def __init__(self, pos=None, context=None):
        self.context = context
        self.pos = pos


    def set_location(self, context, pos):
        self.context = context
        self.pos = pos
        return self


    def __str__(self):
        if self.context:
            return "%sin line %s, column %s => %s" % ('%s ' % self.message if self.message else '', self.pos[0], self.pos[1], self.context)
        else:
            return self.message


class SyntaxError_(VisitorException):

    def __init__(self, message, *args):
        super().__init__(*args)
        self.message = message


class IllegalFunctionCall(VisitorException):
    def __init__(self, message='Illegal function call', *args):
        super().__init__(*args)
        self.message = message


class TranslationError(VisitorException, SemanticError):
    'generic MSX-BASIC translation error'
    def __init__(self, *args):
        if len(args) > 1:
            self.context, self.pos = args
        else:
            self.context, self.pos = None, None


class TokenNotImplementedError(TranslationError):
    def __init__(self, *tokens):
        super().__init__(None, None)
        self.message = "token or token combination '%s' is unknown or not implemented yet" % ' '.join(tokens)


class TypeNotImplementedError(TranslationError):
    def __init__(self, type_name, *args):
        super().__init__(*args)
        self.message = "surrogate type '%s' is unknown or not implemented yet" % type_name


class ScalarInitError(TranslationError):
    def __init__(self, identifier, message=None, context=None, pos=None):
        super().__init__(*args)
        self.message = "cannot initialize %s with scalar value" % identifier


class DimInitAccessError(TranslationError):
    'invalid dim initialisation element'
    def __init__(self, identifier, *arity):
        super().__init__(None, None)
        if len(arity) == 3:
            self.message = "missing initialisation for %s(%s, %s, %s)" % (identifier, arity[0], arity[1], arity[2])
        elif len(arity) == 2:
            self.message = "missing initialisation for %s(%s, %s)" % (identifier, arity[0], arity[1])
        elif len(arity) == 1:
            self.message = "missing initialisation for %s(%s)" % (identifier, arity[0])


class DimRangesMismatch(TranslationError):
    def __init__(self, identifier, *args):
        super().__init__(*args)
        self.message = "'%s' range declaration and initialisation don't match" % identifier


class OutOfBounds(TranslationError):
    def __init__(self, range, *args):
        super().__init__(*args)
        self.message = "Array access out of bounds, should be a value below %s" % range.end


class ParameterCount(TranslationError):
    def __init__(self, expected, value, *args):
        super().__init__(*args)
        self.message = "%s parameters found, but expected %s" % (value, expected)


class TypeMismatch(TranslationError):
    def __init__(self, type1=None, type2=None, identifier=None, **kwargs):
        super().__init__(**kwargs)
        if identifier:
            self.message = "cannot cast '%s' of type '%s' to '%s'" % (identifier, type2.__name__,
                type1.__name__)
        elif type1 and type2:
            self.message = "cannot cast object of type '%s' to '%s'" % (type2.__name__, type1.__name__)
        else:
            self.message = 'no usable type found'


class LoopMismatch(TranslationError):
    'wrong variable name in for loop'
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "no 'For' statement found that matches the 'Next' statement"


class LoopNotFound(TranslationError):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "'Next' without 'For'"


class SelectCaseError(TranslationError):
    'select expected all children to be Case clauses'
    def __init__(self, case, *args):
        super().__init__(*args)
        self.message = "'Select' expected 'Case' clause, got '%s' instead" % case


class NameNotDeclared(TranslationError):
    'variable or label not previously declared'
    def __init__(self, identifier, *args):
        super().__init__(*args)
        self.message = "name '%s' declaration is missing" % identifier


class ReservedName(TranslationError):
    'identifier already in use by built-in function or variable'
    def __init__(self, identifier, *args):
        super().__init__(*args)
        self.message = "reserved identifier '%s' in line %s, column %s" % identifier


class NameRedefined(TranslationError):
    'identifier already declared'
    def __init__(self, identifier, *args):
        super().__init__(*args)
        self.message = "identifier '%s' already declared" % identifier


class InvocationError(TranslationError):
    def __init__(self, name, actual, expected, *args):
        super().__init__(*args)
        self.message = '%s call expected: %s; got %s instead' % (name, actual, expected)


class MissingOperand(TranslationError):
    def __init__(self, complement=None, *args):
        super().__init__(*args)
        self.message = 'Missing operand%s' % ' %s' % complement if complement else ''

