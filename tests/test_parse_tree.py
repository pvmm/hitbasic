import io
import sys
import unittest
import unittest.mock
import arpeggio
import pprint

from os import path
from glob import glob
from contextlib import suppress
from arpeggio import visit_parse_tree
from lib import hitbasic
from lib.visitor import MSXBasicVisitor
from lib.language_statements import *


class TestParseTree(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method_name = args[0]
        self.parser = hitbasic.create_parser()


    def parse(self, text):
        return self.parser.parse(text)


    def parse_file(self, filename):
        return self.parser.parse_file(filename)


    def visit(self, tree):
        return visit_parse_tree(tree, MSXBasicVisitor(parser=self.parser, begin_line=10, debug=False))


    def test_visitor0(self):
        """An empty program is a valid program"""
        tree = self.parse('')
        symbol_table, code = self.visit(tree)
        expected = [('@BeginProgram',), ('@EndProgram',), ('END',)]
        assert code == expected, 'got "%s" as result' % code


    def test_visitor1(self):
        text = """Print 1:Print 2"""
        tree = self.parse(text)
        symbol_table, code = self.visit(tree)
        expected = [('@BeginProgram',), ('PRINT', ' ', 1), ('PRINT', ' ', 2), ('@EndProgram',), ('END',)]
        assert code == expected, 'got "%s" as result' % code


    def test_parse_tree_in_files(self):
        'try to parse all .asc files starting with 1?? in tests/samples'
        test_files = glob(path.join('tests', 'samples', '1??_*.asc'))
        test_files.sort()
        for source_file in test_files:
            s = io.StringIO()
            try:
                tree = self.parse_file(source_file) # looking for matching errors
            except Exception as e:
                raise Exception(source_file)
            symbol_table, code = self.visit(tree)
            pp = pprint.PrettyPrinter(stream=s, width=120)
            pp.pprint(code)
            code = s.getvalue()
            try:
                with open(path.splitext(source_file)[0] + '.objdump', 'r') as obj_file:
                    obj_code = obj_file.read()
                    max = min(len(obj_code), len(code))
                    assert obj_code[:max] == code[:max], 'expected: """\n%s\n""" in file "%s", got """\n%s\n""" instead' % (obj_code, source_file, code) # looking for comparison errors
            except FileNotFoundError as e:
                with open(path.splitext(source_file)[0] + '.objdump', 'w') as obj_file:
                    print(code, file=obj_file)

