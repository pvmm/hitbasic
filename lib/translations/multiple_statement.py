from . import StatementComponents, CodeComponents


class Statement:

    def translate(self):
        return CodeComponents.from_arg_list(*self.code_block).translate()

