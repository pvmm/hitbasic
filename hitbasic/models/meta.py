"Anything else goes here"


from hitbasic import cfg
from hitbasic.models import MetaNode


class EOL(MetaNode):
    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.append("\n")
        return append_to
