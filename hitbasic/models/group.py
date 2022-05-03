# A group stores a block of statements


from hitbasic import cfg
from hitbasic.models import CmdNode
from hitbasic.helpers.list import flatten, interleave


class Group(CmdNode):
    group = True
    sep = f'{cfg.arg_spacing}:{cfg.arg_spacing}'

    def __init__(self, statements=None, **kwargs):
        super().__init__(**kwargs)
        self.statements = statements or []


    def insert(self, pos, stmt):
        self.statements.insert(pos, stmt)


    def append(self, stmt):
        self.statements.append(stmt)


    def __iter__(self):
        return iter(self.statements)


    def printables(self, append_to=None):
        append_to = append_to or []
        for stmt in self:
            try:
                stmt.printables()
            except AttributeError:
                print('no printables() method found in', stmt)
        tmp = interleave([stmt.printables() for stmt in self], self.sep)
        append_to.extend(flatten(tmp))
        return append_to
