import io
import sys
import unittest
import unittest.mock
import arpeggio

from contextlib import suppress
from os import path
from glob import glob
from lib import hitbasic


class TestGrammar(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = hitbasic.create_parser(debug=False)


    def parse(self, text, filename=None):
        return self.parser.parse(text, file_name=filename)


    def parse_file(self, filename):
        return self.parser.parse_file(filename)


    def check_grammar(self, text, expected, filename=None):
        result = '[%s]' % (self.parse(text, filename=filename) if filename else self.parse(text))
        try:
            assert result == expected, 'in file "%s"' % filename
        except AssertionError:
            result = '[%s]' % self.parse(text)
        if filename:
            assert result == expected, 'In "%s" expected "%s"\nBut got "%s"' % (filename, result, expected)
        else:
            assert result == expected, 'Expected "%s"\nBut got "%s"' % (result, expected)


    def test_empty(self):
        'A really empty string this time. Without comments or spaces.'
        result = '[%s]' % self.parse('')
        assert result == '[ | ]'


    def test_no_match_in_files(self):
        'all *.nomatch-asc should trigger arpeggio.NoMatch exception'
        test_files = glob(path.join('tests', 'samples', '*.nomatch-asc'))
        test_files.sort()
        for source_name in test_files:
            with self.assertRaises(arpeggio.NoMatch, msg=source_name):
                self.parse_file(source_name) # looking for matching errors
                raise TypeError(source_name)


    def test_grammar_in_files(self):
        'test all .asc files in tests/samples against their respective .tokens file'
        test_files = glob(path.join('tests', 'samples', '[0-9][0-9].asc'))
        test_files.sort()
        for filename in test_files:
            try:
                with open(filename, 'r') as source_file:
                    source_code = source_file.read()
                    self.parse_file(filename) # looking for matching errors
                with open(path.splitext(filename)[0] + '.tokens', 'r') as token_file:
                    tokens = token_file.read()
                self.check_grammar(source_code, tokens, filename) # looking for comparison errors
            except FileNotFoundError as e:
                with open(filename, 'r') as source_file:
                    source_code = source_file.read()
                    result = '[%s]' % self.parse(source_code)
                with open(path.splitext(filename)[0] + '.tokens', 'w') as token_file:
                    print(result, file=token_file, end='') # generate .tokens file if it doesn't exist
