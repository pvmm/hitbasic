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
        statement = StatementComponents.from_arg_list('FOR', ' ', self.var, ' ', '=', ' ', self.begin, ' ', 'TO', ' ', self.end)
        if self.step != 1: statement.add(' ', 'STEP', ' ', self.step)
        return statement.translate()

