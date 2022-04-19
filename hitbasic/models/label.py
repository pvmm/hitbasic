from hitbasic.models import Node


NUMERIC = 1
PLACEHOLDER = 2


class LabelMark(Node):
    def init(self):
        self.type = PLACEHOLDER if self.identifier else NUMERIC
        self.keyword = self.identifier.upper() if self.identifier else self.line_num
