from . import StatementComponents
from ..hitbasic import Surrogate
from .. import language_statements as statements


class Statement:

    def __init__(self, rule, position, error, target, branch_type=statements.GOTO, *args, **kwargs):
        Surrogate.__init__(self, rule, position, error, target=target, branch_type=branch_type, **kwargs)


    def translate(self):
        return StatementComponents.from_arg_list(self.branch_type, ' ', self.target.identifier).translate()

