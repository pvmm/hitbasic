from . import StatementComponents, CodeComponents


def translate(self):
    """
    @DoLoopStart
    IF NOT(<condition>) THEN @DoLoopEnd
	...
    GOTO @DoLoopStart
    @DoLoopEnd
    """
    statement = StatementComponents.from_arg_list('FOR', ' ', self.var, ' ', '=', ' ', self.begin, ' ', 'TO', ' ', self.end)

    if self.step:
        statement.add(' ', 'STEP', ' ', self.step)

    return CodeComponents().append(statement).translate()

