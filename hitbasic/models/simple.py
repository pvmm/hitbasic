# Statements without parameters


from hitbasic.models import CmdNode


class SimpleStmt(CmdNode):

    def __str__(self):
        return self.keyword.upper()
