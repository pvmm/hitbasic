from . import ClauseComponents
from ..hitbasic import Surrogate


class Clause:

    def __init__(self, rule, position, error, identifier=None, line_number=None, *args, **kwargs):
        'label clauses are used in branch instructions, like in the statement "GOTO EndProgram"'
        if not identifier:
            raise SyntaxError()
        Surrogate.__init__(self, rule, position, error, identifier=identifier, line_number=line_number, **kwargs)


    def translate(self):
        return ClauseComponents(self.line_number if self.line_number else '@%s' % self.identifier)
