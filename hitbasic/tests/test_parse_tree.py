import io
import sys
import unittest
import unittest.mock
#import arpeggio

from os import path
from glob import glob
from contextlib import suppress
#from arpeggio import visit_parse_tree
from hitbasic import hitbasic


class TestParseTree: #(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method_name = args[0]
        self.parser = hitbasic.create_metamodel()


    def visit(self, source):
        'Generate symbol table and intermediate code from string.'
        tree = self.parser.parse(source)
        return visit_parse_tree(tree, MSXBasicVisitor(parser=self.parser, begin_line=10, debug=False))


    def visit_file(self, file_name):
        'Generate symbol table and intermediate code from file.'
        tree = self.parser.parse_file(file_name)
        return visit_parse_tree(tree, MSXBasicVisitor(parser=self.parser, begin_line=10, debug=False))


    def test_visitor0(self):
        'An empty program is a valid program.'
        symbol_table, code = self.visit('')
        expected = [('@BeginProgram',), ('@EndProgram',), ('END',)]
        assert code == expected, 'got "%s" as result' % code


    def test_visitor1(self):
        text = """Print 1:Print 2"""
        symbol_table, code = self.visit(text)
        expected = [('@BeginProgram',), ('PRINT', ' ', '1'), ('PRINT', ' ', '2'), ('@EndProgram',), ('END',)]
        assert code == expected, 'got "%s" as result' % code


    def test_parse_tree_in_files(self):
        'try to parse all .asc files in the nodes directory'
        test_files = glob(path.join('tests', 'samples', 'nodes', '*.asc'))
        test_files.sort()
        for source_file in test_files:
            if source_file.count('.') > 1:
                continue
            try:
                symbol_table, code = self.visit_file(source_file)
            except Exception as e:
                print('* exception captured in "%s"' % source_file, file=sys.stderr)
                raise

        '''
    def test_exception_in_files(self):
        'All *.<exceptionname>.asc files should trigger the respective exception.'
        exception_map = {'typemismatch': TypeMismatch, 'loopnotfound': LoopNotFound}
        for name in exception_map.keys():
            test_files = glob(path.join('tests', 'samples', 'nodes', '*.%s.asc' % name))
            test_files.sort()
            for source_name in test_files:
                with self.assertRaises(exception_map[name], msg=source_name):
                    self.visit_file(source_name)
'''

    def test_parse_tree_comparing_objdump(self):
        'try to parse all .asc files in the nodes directory and compare them with the respective objdump file'
        test_files = glob(path.join('tests', 'samples', 'nodes', '*.asc'))
        test_files.sort()
        for source_file in test_files:
            if source_file.count('.') > 1:
                continue
            try:
                symbol_table, code = self.visit_file(source_file)
                code = str().join(str(code).replace("' '", '␢').split())
                with open(path.splitext(source_file)[0] + '.objdump', 'r') as obj_file:
                    expected = str().join(obj_file.read().replace("' '", '␢').split())
                    assert expected == code, 'expected: """\n%s\n""" in file "%s", got """\n%s\n""" instead' % (expected, source_file, code) # looking for comparison errors
            except FileNotFoundError as e:
                with open(path.splitext(source_file)[0] + '.objdump', 'w') as obj_file:
                    print(code, file=obj_file)
