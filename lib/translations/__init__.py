from ..hitbasic import Surrogate

# TODO: replace those by hitbasic.Surrogate, since they can be a source of circular dependency
from .. import language_tokens as tokens
from .. import language_types as types
from .. import language_clauses as clauses
from .. import language_statements as statements

from ..helper import *


class Sequence_(list):
    'transpiler output as a stream of tokens'
    def __init__(self, components):
        if isinstance(components, (str, int, float, bool)):
            self.append(components)
        else:
            self.add(*components)


    @classmethod
    def from_arg_list(klass, *components):
        return klass(components)


    def add(self, *items):
        for item in items:
            super().append(item)
        return self # allow chain calls


class ClauseComponents(Sequence_):
    def __init__(self, components=()):
        for component in make_tuple(components):
            if isinstance(component, (StatementComponents, ClauseComponents)):
                raise TypeError()
            else:
                self.append(component)


    def add(self, *items):
        for item in items:
            if type(item) == ClauseComponents:
                self.extend(item)
            elif type(item) == tokens.token_type:
                self.extend(item.token)
            elif type(item) in statements.TYPES.values():
                raise TypeMismatch(ClauseComponents.__class__, item)
            else:
                self.append(item)
        return self # allow chain calls


    def translate(self):
        output = []
        for item in self:
            if isinstance(item, (str, int, float, bool)):
                output.append(item)
            elif type(item) in clauses.TYPES.values():
                output.extend(item.translate())
            elif type(item) in types.TYPE_MAPPING.values():
                output.extend(item.translate())
            elif isinstance(item, ClauseComponents):
                output.extend(item.translate())
            elif isinstance(item, (StatementComponents, CodeComponents)):
                raise TypeError()
        return output


class StatementComponents(Sequence_):
    def __init__(self, components=()):
        for component in make_tuple(components):
            if isinstance(component, StatementComponents):
                raise TypeError()
            else:
                self.append(component)


    def add(self, *items):
        for item in items:
            if type(item) == ClauseComponents:
                self.extend(item)
            elif type(item) == tokens.token_type:
                self.append(*item.token)
            else:
                self.append(item)
        return self # allow chain calls


    def translate(self):
        output = []
        for item in self:
            if isinstance(item, (str, int, float, bool)):
                output.append(item)
            elif isinstance(item, ClauseComponents):
                self.extend(item)
            elif isinstance(item, StatementComponents):
                raise TypeError()
            elif type(item) in clauses.TYPES.values():
                output.extend(item.translate())
            elif type(item) in types.TYPES.values():
                output.extend(item.translate())
            elif type(item) in statements.TYPES.values():
                # adding GOSUB to IF-THEN for instance
                output.extend(item.translate())
            else:
                output.append(item.translate())
        return output


class CodeComponents(Sequence_):
    def __init__(self, components=()):
        for component in make_tuple(components):
            if isinstance(component, CodeComponents):
                self.extend(component)
            if isinstance(component, StatementComponents):
                self.append(component)
            elif isinstance(component, ClauseComponents):
                raise TypeError()
            else:
                self.append(component)


    def add(self, *items):
        for item in items:
            if type(item) == tuple:
                self.append(item)
            elif type(item) == StatementComponents:
                self.append(item)
            elif type(item) == CodeComponents:
                self.extend(item)
            elif type(item) in clauses.TYPES.values():
                raise TypeError()
            elif isinstance(item, Surrogate):
                self.append(item)
            else:
                self.append(item)
        return self # allow chain calls


    def translate(self):
        'Output multiple translated read-only statements'
        output = CodeComponents()

        for statement in self:
            result = statement.translate()
            if result: output.add(result)
        return output


    def freeze(self):
        output = CodeComponents()
        for statement in self:
            output.append(tuple(statement))
        return output

