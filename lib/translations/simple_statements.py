from . import StatementComponents
from .. import language_statements as statements


def __eq__(self, other):
    if isinstance(other, statements.Statement):
        return self.tokens == other.tokens
    return False


def translate(self):
    return StatementComponents(self.tokens).translate()

