from hitbasic.models import CmdNode


NUMERIC = 1
PLACEHOLDER = 2


class LabelMark(CmdNode):

    def __init__(self, identifier=None, **kwargs):
        self.identifier = identifier[1:] if identifier.startswith('@') else identifier
        super().__init__(**kwargs)


    def init(self):
        self.type = PLACEHOLDER if self.identifier else NUMERIC
        self.keyword = self.identifier.upper() if self.identifier else self.line_num


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.append(f'@{self.identifier}')
        return append_to
