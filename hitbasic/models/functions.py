# Control structures and related models


from hitbasic import cfg
from hitbasic.helpers import string
from hitbasic.helpers.list import flatten
from hitbasic.models import Node, CmdNode
from hitbasic.models.default import Group
from hitbasic.models.labels import LabelMark
from hitbasic.msx.types import get_type_from_id


class ReturnStmt(CmdNode):
    keyword = 'RETURN'

    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.append(f'{self.keyword}{cfg.spacing}{self.target}')
        return append_to


class FuncStmt(Group):
    multiline = True

    def get_identifier(self):
        return f'@{self.header.name}()'


    def get_params(self):
        return self.header.params


    def get_body(self):
        return self.statements


    def get_return_type(self):
        return self.header.ret.type if self.header.ret else get_type_from_id(self.header.name)


    def processor(self, symbol_table):
        body = self.get_body()
        begin, end = self.get_positions()

        # Add function's entry point
        body.insert(0, LabelMark(self.get_identifier(), parent=self.parent, _tx_position=begin))
        # Add reference to symbol table
        symbol_table.register_function(self.get_identifier(), params=self.get_params(),
                type_=self.get_return_type())

        # TODO: come up with a better job of detecting dangling code paths
        if not isinstance(body[-1], ReturnStmt):
            body.append(ReturnStmt())

        for param in self.header.params:
            type_ = get_type_from_id(param.name)
            var = symbol_table.create_hitbasic_var(type_=type_, inner=True)

        return Group(body)


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.extend(flatten([stmt.printables() for stmt in self.statements]))
        return append_to

