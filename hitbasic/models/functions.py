# Control structures and related models


from hitbasic.helpers import string
from hitbasic.models import Node, CmdNode
from hitbasic import cfg


class FuncStmt(CmdNode):
    multiline = True
