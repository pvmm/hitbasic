# Control structures and related models


from hitbasic import cfg
from hitbasic.helpers import string
from hitbasic.helpers.list import flatten
from hitbasic.models import Node, CmdNode
from hitbasic.models.default import Group
from hitbasic.models.labels import LabelMark
from hitbasic.msx.types import get_type_from_id


def processor(func_stmt, symbol_table):
    body = func_stmt.get_body()
    begin, end = func_stmt.get_positions()

    # Add function's entry point
    body.insert(0, LabelMark(func_stmt.get_identifier(), parent=func_stmt.parent, _tx_position=begin))
    # Add reference to symbol table
    symbol_table.register_function(func_stmt.get_identifier(), params=func_stmt.get_params(),
            type_=func_stmt.get_return_type())

    # TODO: come up with a better job of detecting dangling code paths
    if not isinstance(body[-1], ReturnStmt):
        body.append(ReturnStmt())

    return Group(body)


class ReturnStmt(CmdNode):
    keyword = 'RETURN'


class FuncStmt(CmdNode):
    multiline = True

    def get_identifier(self):
        return f'@{self.header.name}()'


    def get_params(self):
        return self.header.params


    def get_body(self):
        return self.statements


    def get_return_type(self):
        return self.header.ret.type if self.header.ret else get_type_from_id(self.header.name)


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.extend(flatten([stmt.printables() for stmt in self.statements]))
        return append_to
