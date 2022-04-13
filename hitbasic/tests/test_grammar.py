import io
import sys
import unittest
import unittest.mock
import arpeggio

from contextlib import suppress
from os import path
from glob import glob

from hitbasic import hitbasic


class TestGrammar(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metamodel = hitbasic.create_metamodel(debug=False)


    def parse(self, text, file_name=None):
        return self.metamodel.model_from_str(text, file_name=file_name)


    def parse_file(self, file_name):
        return self.metamodel.model_from_file(file_name)


    def check_grammar(self, text, expected, file_name=None):
        result = '[%s]' % (self.parse_file(file_name) if file_name else self.model_from_str(text))
        assert result == expected, 'in file "%s": got "%s" instead.' % (file_name, result)


    def test_empty(self):
        'A really empty string this time. Without comments or spaces.'
        print(self.parse(''))
        result = '[%s]' % self.parse('')
        assert result == '[]', 'got %s instead' % result


    def test_no_match_in_files(self):
        'All *.nomatch.asc should trigger an arpeggio.NoMatch exception.'
        test_files = glob(path.join('hitbasic', 'tests', 'samples', 'grammar', '*.nomatch.asc'))
        test_files.sort()
        for source_name in test_files:
            with self.assertRaises(arpeggio.NoMatch, msg=source_name):
                self.parse_file(source_name) # looking for matching errors
                raise TypeError(source_name)


    def test_grammar_in_files(self):
        'test all .asc files in tests/samples against their respective .tokens file'
        test_files = glob(path.join('hitbasic', 'tests', 'samples', 'grammar', '*.asc'))
        test_files.sort()
        for file_name in test_files:
            print(f'\nTesting file {file_name}...')
            if file_name.endswith('.nomatch.asc'):
                continue
            try:
                with open(file_name, 'r') as source_file:
                    source_code = source_file.read()
                    try:
                        x = self.parse_file(file_name) # looking for matching errors
                        print(type(x))
                    except Exception as e:
                        print('* exception captured in "%s"' % file_name, file=sys.stderr)
                        raise
                    continue
                with open(path.splitext(file_name)[0] + '.tokens', 'r') as token_file:
                    tokens = token_file.read()
                self.check_grammar(source_code, tokens, file_name) # looking for comparison errors
            except FileNotFoundError as e:
                with open(file_name, 'r') as source_file:
                    source_code = source_file.read()
                    result = '[%s]' % self.model_from_str(source_code)
                with open(path.splitext(file_name)[0] + '.tokens', 'w') as token_file:
                    print(result, file=token_file, end='') # generate .tokens file if it doesn't exist
