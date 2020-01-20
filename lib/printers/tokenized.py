import sys
import io
import re
from label import Label
from subroutines import Function
from keywords import Instruction
from expressions import Operation
from structures import Condition
from non_literals import Variable
from literals import Number, String
from prints import LineMarker

class ExprTokenizer:
    TOKENIZER = { 'CHR': 0x16, 'CHR$': 0x16 }

    def __init__(self, node):
        if isinstance(node, Variable):
            pass
        elif isinstance(node, Operation):
            pass
        elif isinstance(node, FunctionCall):
            pass


class NodeTokenizer:
    """ """
    # From the MSX Red Book
    TOKENIZER = { 'PRINT': 0x91, 'GOTO': 0x89 }

    def __init__(self, node):
        self.node = node
        l = 0
        if isinstance(node, Instruction):
            self._len += len(node.keywords)
            for k in node.keywords:
                self._str += TOKENIZER[node.name.upper()]

            self.params = []
            # TODO check difference between code block and expression
            for p in node.params:
                p = ExprTokenizer(p)
                self.params.append(p)
                self._str += str(p)


    def __len__(self):
        return self._len


class Generator:
    """Generate tokenized MSX-BASIC file."""

    def __init__(self, file, line_start=10, line_inc=10, starting_addr=0x8000):
        self.file = file
        self.line_start = line_start
        self.line_inc = line_inc
        self.starting_addr = starting_addr
        self._labels = {}


    def store_new_label(self, line_num, name):
        self._labels[name] = line_num


    def first_pass(self, nodes):
        pos = 0
        line_num = self.line_start
        line_len = 0
        node_iter = iter(nodes)
        while node_iter:
            try:
                n = next(node_iter)
                if isinstance(n, Label):
                    self.store_new_label(line_num, n.name)
                    # Adding line marker breaks the line
                    if not isinstance(self.previous_node, Label):
                        nodes.insert(pos, LineMarker(line_num, line_addr=self.line_addr)); pos += 1
                        line_num += self.line_inc
                    line_len = 0
                else:
                    # Replace node with tokenized element
                    n = NodeTokenizer(n)
                    nodes[pos] = n

                # Line too long? Break it
                if line_len + len(n) >= 254:
                    self.line_addr += line_len
                    # Adding line marker breaks the line
                    nodes.insert(pos, LineMarker(line_num, line_addr=self.line_addr)); pos += 1
                    line_num += self.line_inc
                    line_len = 0
                else:
                    line_len += len(n)

                pos += 1
            except StopIteration:
                break


    def printable_linemark(self, node):
        s = io.stringIO()
        print(node.start_addr & 0xff, (node.start_addr >> 8) & 0xff, sep='', file=s)
        return s.getvalue()


    def print(nodes=[]):
        self.first_pass(nodes)

        for node in nodes:
            # print next line's memory address (2 bytes)
            print(node, sep='')

