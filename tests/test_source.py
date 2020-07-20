import io
import os
import sys
import unittest
import unittest.mock
import arpeggio

from os import path
from glob import glob
from contextlib import suppress
from arpeggio import visit_parse_tree
from lib import hitbasic

from lib.visitor import MSXBasicVisitor
from lib.language_statements import *
from lib.printers.text import Generator as TextGenerator


class TestSource(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method_name = args[0]
        self.parser = hitbasic.create_parser()


    def generate_source(self, filename):
        'Generate MSX-BASIC source for ASC file as input.'
        tree = self.parser.parse_file(filename)
        symbol_table, code = visit_parse_tree(tree, MSXBasicVisitor(parser=self.parser, begin_line=10, debug=False))
        output = io.StringIO()
        TextGenerator(symbol_table, output).print(code)
        return output.getvalue()


    def test_source00(self):
        'An empty program is a valid program.'
        test_file = path.join('tests', 'samples', 'sources', '00_empty.asc')
        source = self.generate_source(test_file)
        assert source == "10 END\n", 'got "%s" as result' % source
