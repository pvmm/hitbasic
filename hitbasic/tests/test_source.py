import io
import os
import sys
import unittest
import unittest.mock

from os import path
from glob import glob
from contextlib import suppress
from hitbasic import hitbasic


class TestSource: #(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method_name = args[0]
        self.metamodel = hitbasic.create_metamodel()


    def generate_source(self, filename):
        'Generate MSX-BASIC source for ASC file as input.'
        tree = self.parser.parse_file(filename)
        symbol_table, code = visit_parse_tree(tree, MSXBasicVisitor(parser=self.parser, begin_line=10, debug=False))
        output = io.StringIO()
        TextGenerator(symbol_table, output).print(code)
        return output.getvalue()


    def test_source00(self):
        'An empty program is a valid program.'
        test_file = path.join('hitbasic', 'tests', 'samples', 'sources', '00_empty.asc')
        source = self.generate_source(test_file)
        assert source == "10 END\n", 'got "%s" as result' % source


    def test_source_from_file(self):
        'try to parse all .asc files in the sources directory and compare them with the respective preexisting .asc file'
        test_files = glob(path.join('hitbasic', 'tests', 'samples', 'sources', '*.asc'))
        test_files.sort()
        for source_file in test_files:
            if source_file.endswith('.result.asc'):
                continue
            source = self.generate_source(source_file)
            try:
                with open(path.splitext(source_file)[0] + '.result.asc', 'r') as obj_file:
                    result = obj_file.read()
                    assert source == result, 'expected: """\n%s\n""" in file "%s", got """\n%s\n""" instead' % (result, source_file, source) # looking for comparison errors
            except FileNotFoundError as e:
                with open(path.splitext(source_file)[0] + '.result.asc', 'w') as obj_file:
                    print(source, file=obj_file, end='')
