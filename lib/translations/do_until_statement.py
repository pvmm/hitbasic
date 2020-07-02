from . import StatementComponents, CodeComponents


class Statement:

    def translate(self):
        """
        @DoLoopStart
        IF NOT(<condition>) THEN @DoLoopEnd
    	...
        GOTO @DoLoopStart
        @DoLoopEnd
        """
        code = CodeComponents(self.start_label)
        code.append(StatementComponents.from_arg_list('IF', ' ', 'NOT', '(', self.expression, ')', ' ', 'THEN', ' ', self.exit_branch))

        for statement in self.code_block:
            code.append(statement)

        code.append(self.continue_branch)
        code.append(self.end_label)

        return code.translate()

