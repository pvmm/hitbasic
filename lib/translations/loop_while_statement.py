from . import StatementComponents, CodeComponents


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

    return code.append(StatementComponents.from_arg_list('IF', ' ', self.expression, ' ', 'THEN', ' ', self.branch)).translate()

