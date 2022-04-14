# Statements without parameters

class SimpleStmt(object):
    def __init__(self, parent, keyword):
        self.parent = parent
        self.keyword = keyword

    def __str__(self):
        return "{}".format(self.keyword)

    def write(self, file):
        pass
