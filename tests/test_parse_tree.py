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


    def test_label_comparation1(self):
        """An empty program is a valid program"""
        tree = self.parse('')
        result = self.visit(tree)
        expected = Label('BeginProgram', type=Label.BEGIN_PROGRAM)
        assert result[0] == expected, 'got "%s" as result' % result[0]


    def test_label_comparation2(self):
        """An empty program is a valid program"""
        tree = self.parse('')
        result = self.visit(tree)
        expected = Label('BeginProgram', type=Label.INTERNAL)
        assert result[0] != expected, 'got "%s" as result' % result[0]


    def test_label_comparation3(self):
        """An empty program is a valid program"""
        tree = self.parse('')
        result = self.visit(tree)
        expected = Label('BeginProgram', type=Label.END_PROGRAM)
        assert result[0] != expected, 'got "%s" as result' % result[0]


    def test_label_comparation4(self):
        """An empty program is a valid program"""
        tree = self.parse('')
        result = self.visit(tree)
        expected = Label('BeginProgram', type=Label.USER_DEFINED)
        assert result[0] != expected, 'got "%s" as result' % result[0]


    def test_label_comparation5(self):
        """An empty program is a valid program"""
        tree = self.parse('')
        result = self.visit(tree)
        expected = Label('EndProgram', type=Label.END_PROGRAM)
        assert result[1] == expected, 'got "%s" as result' % result[0]


    def test_visit_empty_grammar(self):
        """An empty program is a valid program"""
        tree = self.parse('')
        result = self.visit(tree)
        expected = [Label('BeginProgram', type=Label.BEGIN_PROGRAM), Label('EndProgram', type=Label.END_PROGRAM), Instruction('End')]
        assert result == expected, 'got "%s" as result' % result 


    def test_visitor1(self):
        text = """Print 1:Print 2"""
        tree = self.parse(text)
        result = self.visit(tree)
        expected = [Label('BeginProgram', type=Label.BEGIN_PROGRAM), Instruction('Print', parameters=(Number(1),)), Instruction('Print', parameters=(Number(2),)),
                Label('EndProgram', type=Label.END_PROGRAM), Instruction('End')]
        assert result == expected, 'got "%s" as result' % result


    def test_visitor2(self):
        pass

