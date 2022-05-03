# Control structures and related models


from hitbasic import cfg
from hitbasic.helpers import string
from hitbasic.helpers.list import flatten
from hitbasic.models import Node, CmdNode, find_parent_type
from hitbasic.models.default import Group, AssignStmt, processor
from hitbasic.models.labels import LabelMark
from hitbasic.msx import types


class ReturnStmt(CmdNode):
    keyword = 'RETURN'

    def processor(self, symbol_table):
        if self.expr:
            func_stmt = find_parent_type(FuncStmt, self)
            assert func_stmt, 'function declaration not found'

            group = Group([])
            for var in func_stmt.header.get_return_vars():
                group.append(AssignStmt(var, self.expr))
            return group

        return self


    def printables(self, append_to=None):
        append_to = append_to or []
        if hasattr(self, 'target'):
            append_to.append(f'{self.keyword}{cfg.spacing}{self.target}')
        else:
            append_to.append(f'{self.keyword}')
        return append_to


class FuncHead(Node):
    def init(self):
        self.param_vars = []
        self.return_vars = []


    def get_param_types(self):
        param_types = []
        for param in self.params:
            param_types.append(param.type)
        return param_types


    def get_param_vars(self):
        param_vars = []
        for param in self.params:
            param_vars.append(param.identifier)
        return param_vars


    def get_return_types(self):
        return [self.ret.type] if self.ret else [types.get_type_from_id(self.identifier)]


    def get_return_vars(self):
        return self.return_vars


    def processor(self, symbol_table):
        func_stmt = self.parent
        assert func_stmt, 'function declaration not found'

        # TODO multiple return types support
        #for var in self.ret.types_:
        #for type_ in self.get_return_types():
        var = symbol_table.create_hitbasic_var(self.identifier, type_=self.get_return_types()[0], inner=False)

        # Internal variable for each parameter
        for var in self.params:
            var = symbol_table.create_hitbasic_var(var.identifier, type_=var.type, inner=True)
            self.param_vars.append(var)

        # Internal variable for return value
        for type_ in self.get_return_types():
            self.return_vars.append(symbol_table.create_hitbasic_var(type_=type_, inner=True))

        return self


class FuncStmt(Group):
    multiline = True

    def get_identifier(self):
        return f'@{self.header.identifier}()'


    def get_body(self):
        return self.statements


    def processor(self, symbol_table):
        body = self.get_body()
        begin, end = self.get_positions()

        # Add internal function params as variables
        #for param in self.header.params:
        #    body.insert(0, AssignStmt(param.name, ))

        # Add function's entry point
        body.insert(0, LabelMark(self.get_identifier(), parent=self.parent, _tx_position=begin))
        # Add reference to symbol table
        symbol_table.register_function(self.get_identifier(), params=self.header.params,
                type_=self.header.get_return_types())

        # TODO: come up with a better job of detecting dangling code paths
        if not isinstance(body[-1], ReturnStmt):
            body.append(ReturnStmt())

        return Group(body)


    def printables(self, append_to=None):
        append_to = append_to or []
        append_to.extend(flatten([stmt.printables() for stmt in self.statements]))
        return append_to

