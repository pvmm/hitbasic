from arpeggio import SemanticError


class VisitorException(Exception):
    'exception thrown inside a visitor'
    def __init__(self, filename=None, context=None, pos=None):
        self.filename = filename
        self.context = context
        self.pos = pos


    @property
    def message(self):
        return self._message if self._message else self.__class__.__name__


    @message.setter
    def message(self, value):
        self._message = value


    def set_location(self, filename=None, context=None, pos=None):
        self.filename = filename
        self.context = context
        self.pos = pos
        return self # chain


    def __str__(self):
        if self.context:
            return '%s in%sline %s, column %s => %s' % (self.message,
                    (' file: "%s" ' % self.filename) if self.filename else ' ',
                    self.pos[0], self.pos[1], self.context)
        else:
            return self.message


class SyntaxError_(VisitorException):

    def __init__(self, message, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = message


class IllegalFunctionCall(VisitorException):
    def __init__(self, message='Illegal function call', filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = message


class TranslationError(VisitorException, SemanticError):
    'generic MSX-BASIC translation error'
    def __init__(self, filename=None, context=None, pos=None):
        self.filename = filename
        self.context = context
        self.pos = pos


class TokenNotImplementedError(TranslationError):
    def __init__(self, *tokens, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "token or token combination '%s' is unknown or not implemented yet" % ' '.join(tokens)


class TypeNotImplementedError(TranslationError):
    def __init__(self, type_name, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "surrogate type '%s' is unknown or not implemented yet" % type_name


class ScalarInitError(TranslationError):
    def __init__(self, identifier, message=None, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "cannot initialize %s with scalar value" % identifier


class DimInitAccessError(TranslationError):
    'invalid dim initialisation element'
    def __init__(self, identifier, *arity, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        if len(arity) == 3:
            self.message = "missing initialisation for %s(%s, %s, %s)" % (identifier, arity[0], arity[1], arity[2])
        elif len(arity) == 2:
            self.message = "missing initialisation for %s(%s, %s)" % (identifier, arity[0], arity[1])
        elif len(arity) == 1:
            self.message = "missing initialisation for %s(%s)" % (identifier, arity[0])


class DimRangesMismatch(TranslationError):
    def __init__(self, identifier, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "'%s' range declaration and initialisation don't match" % identifier


class OutOfBounds(TranslationError):
    def __init__(self, range, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "Array access out of bounds, should be a value below %s" % range.end


class ParameterCount(TranslationError):
    def __init__(self, expected, value, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "%s parameters found, but expected %s" % (value, expected)


class TypeMismatch(TranslationError):
    def __init__(self, type1=None, type2=None, identifier=None, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        if identifier:
            self.message = "cannot cast '%s' of type '%s' to '%s'" % (identifier, type2.__name__,
                type1.__name__)
        elif type1 and type2:
            self.message = "cannot cast object of type '%s' to '%s'" % (type2.__name__, type1.__name__)
        else:
            self.message = 'no usable type found'


class LoopMismatch(TranslationError):
    'wrong variable name in for loop'
    def __init__(self, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "no 'For' statement found that matches the 'Next' statement"


class LoopNotFound(TranslationError):
    def __init__(self, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "'Next' without 'For'"


class SelectCaseError(TranslationError):
    'select expected all children to be Case clauses'
    def __init__(self, case, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "'Select' expected 'Case' clause, got '%s' instead" % case


class NameNotDeclared(TranslationError):
    'variable or label not previously declared'
    def __init__(self, identifier, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "name '%s' declaration is missing" % identifier


class ReservedName(TranslationError):
    'identifier already in use by built-in function or variable'
    def __init__(self, identifier, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "reserved identifier '%s' in line %s, column %s" % identifier


class NameRedefined(TranslationError):
    'identifier already declared'
    def __init__(self, identifier, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = "identifier '%s' already declared" % identifier


class InvocationError(TranslationError):
    def __init__(self, name, actual, expected, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = '%s call expected: %s; got %s instead' % (name, actual, expected)


class MissingOperand(TranslationError):
    def __init__(self, complement=None, filename=None, context=None, pos=None):
        super().__init__(filename, context, pos)
        self.message = 'Missing operand%s' % ' %s' % complement if complement else ''
