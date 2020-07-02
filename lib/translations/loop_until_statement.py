from . import StatementComponents, CodeComponents


class Statement:

    def translate(self):
        """
        @DoLoopStart
    	...
        IF NOT(<condition>) THEN @DoLoopStart
        @DoLoopEnd
        """
        code = CodeComponents(self.do_loop_start)

        for statement in self.code_block:
            code.add(statement)

        return code.add(StatementComponents.from_arg_list('IF', ' ', 'NOT', '(', self.expression, ')', ' ', 'THEN', ' ', self.branch)).translate()

