from . import StatementComponents, CodeComponents


class Statement:

    def translate(self):
        """
        @DoLoopStart
    	...
        IF <condition> THEN @DoLoopStart
        @DoLoopEnd
        """
        code = CodeComponents(self.do_loop_start)

        for statement in self.code_block:
            code.append(statement)

        loop_test = StatementComponents.from_arg_list('IF', ' ', self.expression, ' ', 'THEN', ' ', self.branch)
        return code.add(loop_test).translate()
