import sys
import io
import re
from contextlib import suppress
from nodes import *
from priority import PRIORITY
from . import LineMarker

class Generator:
    LINE_MAX = 255

    def __init__(self, symbol_table, file, line_start=10, line_inc=10, line_len=255):
        print("symbol_table = ", symbol_table)
        self.symbol_table = symbol_table
        self.file = file
        self.line_start = line_start
        self.line_inc = line_inc
        self.line_max = line_len or Generator.LINE_MAX
        self.new_line = False
        self.line_num = 0
        self.context = '_global'
        self.labels = {}


    def get_name(self, name):
        with suppress(KeyError):
            return self.symbol_table[self.context][name]
        with suppress(KeyError):
            if self.context != '_global':
                return self.symbol_table['_global'][name]
        raise Exception('name "%s" not defined' % name)


    def check_space(self, code):
        if isinstance(code, list):
            for c in code:
                print(c, ':', type(c))
            return self.line_len + sum([len(c) for c in code]) <= self.line_max
        else:
            return self.line_len + len(code) <= self.line_max


    def store_label(self, name, line_number=None):
        self.labels[name] = Label(name, line_number=line_number)


    def convert_keywords(self, keywords):
        """Convert keywords into printable code"""
        code = []
        for k in keywords:
            code.append(k.upper())
        return code


    def convert_expr(self, node):
        """Convert expression node into printable code"""
        code = []
        print("convert_expr received", node, type(node))
        if isinstance(node, Number):
            code = [node.value]
        elif isinstance(node, String):
            code = ['"%s"' % node.value]
        elif isinstance(node, Variable):
            code = [node.name]
            if node.params:
                code += ['(']
                for p in node.params:
                    code += self.convert_expr(p)
                code += [')']
            if isinstance(node, RVariable):
                obj = self.get_name(node.name)
                # TODO add function call interface code
                if type(obj) == Function:
                    code.extend(self.convert_function_call(obj))
        elif isinstance(node, Operation):
            # left operand
            c = self.convert_expr(node.op1)
            if type(node.op1) == Operation and PRIORITY[node.op1.op] < PRIORITY[node.op]:
                code.append('(')
                code.extend(c)
                code.append(')')
            else:
                code.extend(c)
            # operator
            code.append(node.op)
            # right operand
            c = self.convert_expr(node.op2)
            if type(node.op2) == Operation and PRIORITY[node.op2.op] < PRIORITY[node.op]:
                code.append('(')
                code.extend(c)
                code.append(')')
            else:
                code.extend(c)
        else:
            raise TypeError('not an valid expression: %s' % repr(node))
        #print('convert_expr returns', code)
        return code


    def convert_node(self, node):
        """Convert node into mixed representation"""
        code = []
        if type(node) == Label:
            pass
        elif type(node) == Function:
            for n in node.body:
                code = self.convert_node(n)
                code.extend(code)
        elif type(node) == Command:
            if node.infix:
                c = self.convert_expr(node.params[0])
                c += self.convert_keywords(node.keywords)
                c += self.convert_expr(node.params[1])
                code.extend(c)
            else:
                code.extend(self.convert_keywords(node.keywords))
                for p in node.params:
                    if type(p) in [Operation, Variable, Number, String]:
                        code.extend(self.convert_expr(p))
                    else:
                        # space, newline, comma, semicolon...
                        code.append(p)
        else:
            code.append(node)
        #print('convert_node returns', node)
        return code


    def convert_nodes(self, nodes, last_node=None):
        last_node = last_node
        code = []
        for n in nodes:
            if type(last_node) == Command:
                code.append(':')
            code.extend(self.convert_node(n))
            last_node = n
        return code


    def write_start(self, line_num=None):
        """Write program start"""
        self.line_num = self.line_start
        self.code = []
        self.subroutines = []
        code = [str(self.line_num), ' ']
        self.line_len = sum([len(c) for c in code])
        self.write_code(code)


    def find_label(self, nodes):
        for n in nodes:
            if type(n) == Label: return True
        return False


    def write_condition(self, node, last_node=None):
        """Write condition as mixed code representation"""
        external_body = self.find_label(node.then_block)
        if not external_body and node.else_block:
            external_body = self.find_label(node.else_block)

        if isinstance(last_node, Command):
            if self.check_space(':'):
                code = [':', 'IF']
            else:
                self.write_condition(node)
                return None
        else:
            code = ['IF']
        code.extend(self.convert_expr(node.expression))
        code.append('THEN')

        # Retry if there is no space
        if not self.check_space(code):
            self.write_nl()
            self.write_condition(node)
            return None

        if not external_body:
            block = self.convert_nodes(node.then_block)
            if node.else_block:
                block.append('ELSE')
                block.extend(self.convert_nodes(node.else_block))
            external_body = not self.check_space(block)
            if not external_body:
                code.extend(block)
                self.write_code(code)
                self.write_nl()
                return None

        if external_body:
            code[-1] = 'GOTO' # Remove THEN and replace with GOTO
            then_label = self.create_label('Then')
            # write then block 
            code.extend(['GOTO', then_label])
            node.then_block.insert(0, then_label)
            node.then_block.append('RETURN')
            self.subroutines.append(node.then_block)
            # write else block 
            if node.else_block:
                else_label = self.create_label('Else')
                code.extend(['ELSE', else_label])
                node.else_block.insert(0, else_label)
                node.else_block.append('RETURN')
                self.subroutines.append(node.else_block)
            # Retry if there is no space
            if not self.check_space(code):
                self.write_nl()
                self.write_condition(node)
                return None
            self.write_nl()
            self.write_code(code)


    def write_nl(self):
        """Write newline"""
        print('line_num = %s', self.line_num)
        self.line_num += self.line_inc
        code = ['\n', str(self.line_num), ' ']
        self.line_len = sum([len(c) for c in code])
        self.write_code(code)


    def write_label(self, label=None, prefix=None, last_node=None):
        if label and prefix:
            raise ValueError("can't use label and prefix together")
        if not isinstance(last_node, Label):
            self.write_nl()
        if label:
            self.store_label(label.name, self.line_num)
        elif prefix:
            self.store_label(prefix, self.line_num)
        else:
            self.store_label('label', self.line_num)


    def write_code(self, node, last_node=None):
        if not isinstance(node, list):
            node = [node]
        for n in node:
            if type(n) == Label:
                self.write_label(label=n, last_node=last_node)
            else:
                code = self.convert_node(n)
                if isinstance(last_node, Command):
                    if self.check_space(':'):
                        self.code.append(':')
                    else:
                        self.write_nl()
                if self.check_space(code):
                    self.code.extend(code)
                    self.line_len += sum([len(c) for c in code])
                else:
                    raise ValueError('line too long')


    def write_mix(self, node, last_node=None):
        """Write mix of printable code and objects"""
        #print('mix =', node, self.last_node)
        if isinstance(node, Function):
            self.subroutines.append((node.name, node.body))
        elif isinstance(node, Condition):
            self.write_condition(node, last_node)
        else:
            self.write_code(node, last_node=last_node)


    def write_all_code(self, nodes):
        """Write the BASIC program"""
        last_node = Label(None)
        self.write_start()
        for n in nodes:
            self.write_mix(n, last_node=last_node)
            last_node = n
        # Write subroutines extracted from nodes
        print(repr(self.subroutines))
        for duple in self.subroutines:
            last_node = None
            self.context, nodes = duple
            for n in nodes:
                self.write_mix(n, last_node=last_node)
                last_node = n


    def first_pass(self, nodes):
        """Collect labels"""
        for n in nodes:
            if isinstance(n, Label):
                self.store_label(n)


    def word_boundaries(self, prev, next):
        return (bool(re.match(r'[a-zA-Z0-9]', prev[-1])
            and bool(re.match(r'[a-zA-Z0-9]', next[0]))))


    def print(self, nodes=[]):
        print(repr(nodes))
        self.first_pass(nodes)
        self.code = []
        self.write_all_code(nodes)

        p = lambda *args, **kwargs: print(*args, **kwargs, sep='', end='', file=self.file)
        for c in self.code:
            #try: print('**', c) except TypeError: print('**', repr(c))
            p(c)
        p('\n')

