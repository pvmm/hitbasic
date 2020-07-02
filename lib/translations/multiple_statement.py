from . import StatementComponents, CodeComponents


class Statement:

    def translate(self):
        return CodeComponents(self.code_block).translate()

