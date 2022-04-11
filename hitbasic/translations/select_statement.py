from . import StatementComponents, CodeComponents


class Statement:

    def translate(self):
        return StatementComponents.from_arg_list('SELECT', 'CASE', self.sel).translate()

