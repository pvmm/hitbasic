from . import StatementComponents, CodeComponents


def translate(self):
    return CodeComponents(self.code_block).translate()

