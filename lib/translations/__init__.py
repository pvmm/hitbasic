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
    'bits and pieces of a statement'
    def __init__(self, components=()):
        if isinstance(components, ClauseComponents):
            self.extend(components)
        elif isinstance(components, (StatementComponents, CodeComponents)):
            raise TypeMismatch(ClauseComponents.__class__, components)
        else:
            for item in make_tuple(components):
                if isinstance(item , ClauseComponents):
                    self.extend(item)
                if isinstance(item, (StatementComponents, ClauseComponents)):
                    raise TypeMismatch(ClauseComponents.__class__, item)
                else:
                    self.append(item)


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
        output = ClauseComponents()
        for item in self:
            if isinstance(item, (str, int, float, bool)):
                output.append(item)
            elif type(item) in clauses.TYPES.values():
                output.extend(item.translate())
            elif type(item) in types.TYPES.values():
                output.append(item.translate())
            elif isinstance(item, ClauseComponents):
                output.extend(item.translate())
            elif isinstance(item, (StatementComponents, CodeComponents)):
                raise TypeMismatch(ClauseComponents.__class__, item)
        return output


class StatementComponents(Sequence_):
    'a single statement'
    def __init__(self, components=()):
        if isinstance(components, ClauseComponents):
            self.extend(components)
        elif isinstance(components, StatementComponents):
            self.extend(components)
        elif isinstance(components, CodeComponents):
            raise TypeMismatch(ClauseComponents.__class__, components)
        else:
            for item in make_tuple(components):
                if isinstance(item, StatementComponents):
                    raise TypeMismatch(ClauseComponents.__class__, item)
                else:
                    self.append(item)


    def add(self, *items):
        for item in items:
            if isinstance(item, (ClauseComponents, StatementComponents)):
                self.extend(item)
            elif type(item) == CodeComponents:
                raise TypeMismatch(StatementComponents.__class__, item)
            elif type(item) == tokens.token_type:
                self.append(*item.token)
            else:
                self.append(item)
        return self # allow chain calls


    def translate(self):
        output = ClauseComponents()
        for item in self:
            if isinstance(item, (str, int, float, bool)):
                output.append(item)
            elif type(item) in clauses.TYPES.values():
                output.extend(item.translate())
            elif type(item) in types.TYPE.values():
                output.extend(item.translate())
            elif isinstance(item, ClauseComponents):
                output.extend(item.translate())
            elif isinstance(item, (StatementComponents, CodeComponents)):
                raise TypeMismatch(StatementComponents.__class__, item)
        return output


    def translate(self):
        output = StatementComponents()
        for item in self:
            if isinstance(item, (str, int, float, bool)):
                output.append(item)
            elif isinstance(item, ClauseComponents):
                self.extend(item.translate())
            elif isinstance(item, CodeComponents):
                raise TypeMismatch(StatementComponents.__class__, item)
            elif type(item) in types.TYPES.values():
                output.append(item.translate())
            elif type(item) in clauses.TYPES.values():
                output.extend(item.translate())
            elif type(item) in statements.TYPES.values():
                output.extend(item.translate())
            else:
                output.append(item.translate())
        return output


class CodeComponents(Sequence_):
    'multi-statement components'
    def __init__(self, components=()):
        if isinstance(components, StatementComponents):
            self.append(components)
        elif isinstance(components, CodeComponents):
            self.extend(components)
        elif isinstance(components, ClauseComponents):
            raise TypeMismatch(CodeComponents.__class__, components)
        else:
            components = make_tuple(components)
            for component in components:
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
                raise TypeMismatch(CodeComponents.__class__, item)
            elif isinstance(item, Surrogate):
                self.append(item)
            else:
                self.append(item)
        return self # allow chain calls


    def translate(self):
        'Output multiple translated read-only statements'
        output = CodeComponents()
        old_result = None
        for statement in self:
            try:
                result = statement.translate()
            except TypeError:
                raise RuleNotImplementedYet(statement, context=old_result)
            if result and type(result) == CodeComponents:
                output.extend(result)
            elif result: output.append(result)
            old_result = result
        return output


    def freeze(self):
        output = CodeComponents()
        for statement in self:
            output.append(tuple(statement))
        return output
