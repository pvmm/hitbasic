# Statements without parameters

from hitbasic.models import Node
from hitbasic import spacing


class SimpleStmt(Node):
    def __str__(self):
        return self.keyword
