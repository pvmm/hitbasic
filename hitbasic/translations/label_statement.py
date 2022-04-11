from . import StatementComponents

from ..hitbasic import Surrogate


class Statement:

    def __init__(self, rule, position, error, identifier, line_number=None, *args, **kwargs):
        'Label statements will be transformed into line numbers in the code and they start with an at-sign'
        Surrogate.__init__(self, rule, position, error, identifier=identifier, line_number=line_number, **kwargs)


    @property
    def id(self):
        return self.identifier


    def __str__(self):
        return 'Label(@%s)' % self.identifier


    def __repr__(self):
        return str(self)


    def translate(self):
        return StatementComponents('@%s' % self.identifier)

