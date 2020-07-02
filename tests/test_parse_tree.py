import sys
import unittest

from os import path
from arpeggio import visit_parse_tree
from lib import hitbasic
from lib.visitor import MSXBasicVisitor
from lib.language_statements import *


class TestParseTree(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method_name = args[0]
        self.parser = hitbasic.create_parser()


    def parse(self, text, debug=False):
        return self.parser.parse(text)


    def visit(self, tree):
        return visit_parse_tree(tree, MSXBasicVisitor(parser=self.parser, begin_line=10, debug=False))


    def test_visitor0(self):
        """An empty program is a valid program"""
        tree = self.parse('')
        result = self.visit(tree)
        expected = [('@BeginProgram',), ('@EndProgram',), ('END',)]
        try:
            assert result[0] == expected, 'got "%s" as result' % result[0]
        except TypeError as e:
            print(e, "\n%s" % result[0])


    def test_visitor1(self):
        text = """Print 1:Print 2"""
        tree = self.parse(text)
        result = self.visit(tree)
        expected = [('@BeginProgram',), ('PRINT', ' ', 1), ('PRINT', ' ', 2), ('@EndProgram',), ('END',)]
        try:
            assert result[0] == expected, 'got "%s" as result' % result[0]
        except TypeError as e:
            print(e, "\n%s" % result[0])

