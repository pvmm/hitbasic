# Statements without parameters


from hitbasic.models import CmdNode


class SimpleStmt(CmdNode):
    def __init__(self, keyword, **kwargs):
        super().__init__(**kwargs)
        self.keyword = keyword


    def __str__(self):
        return self.keyword.upper()
