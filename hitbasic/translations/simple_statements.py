from . import StatementComponents
from .. import language_statements as statements


class Statement:

    def __eq__(self, other):
        if isinstance(other, str):
            return ' '.join(self.tokens).upper() == other.upper()
        if isinstance(other, statements.Statement):
            return self.tokens == other.tokens
        return False


    def translate(self):
        return StatementComponents(self.tokens).translate()
