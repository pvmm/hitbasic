from . import StatementComponents


class Statement:

    def translate(self):
        statement = StatementComponents.from_arg_list('IF', ' ', self.expression, ' ', 'THEN')

        if self.then_branch:
            statement.add(' ', self.then_branch)

        if hasattr(self, 'else_branch') and self.else_branch:
            statement.add(' ', 'ELSE', ' ', self.else_branch, '\n')
        else:
            statement.append('\n') # force newline

        return statement.translate()

