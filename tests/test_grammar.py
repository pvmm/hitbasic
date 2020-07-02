import io
import sys
import unittest
import unittest.mock
import arpeggio

from contextlib import suppress
from os import path
from glob import glob
from lib import hitbasic


captured_output = io.StringIO()

class blah(unittest.TestCase):
    @staticmethod
    def monkey_patch_stderr(original_function):
        """
        :param original_function: Decorated function which is expected to have stderr
        :return: Wrapped function which uses monkey patching for the sys.stderr object
        """
        def wrapper_function(*args, **kwargs):
            my_stderr = sys.stderr
            my_stdout = sys.stdout
            sys.stderr = captured_output
            sys.stdout = captured_output
            return_value = original_function(*args, **kwargs)
            sys.stderr = my_stderr
            sys.stdout = my_stdout
            return return_value
        return wrapper_function


class TestGrammar(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = hitbasic.create_parser(debug=False)


    def parse(self, text):
        return self.parser.parse(text)


    def check_grammar(self, text, expected, filename=None):
        result = '[%s]' % self.parse(text)
        try:
            assert result == expected
        except AssertionError:
            result = '[%s]' % self.parse(text)
            #print('\n%s' % result)
        if filename:
            assert result == expected, 'In "%s" expected "%s"\nBut got "%s"' % (filename, result, expected)
        else:
            assert result == expected, 'Expected "%s"\nBut got "%s"' % (result, expected)


    def test_empty(self):
        'A really empty string this time. Without comments and stuff.'
        result = '[%s]' % self.parse('')
        assert result == '[ | ]'


    def test_error01(self):
        """Invalid instruction between Prints"""
        with suppress(arpeggio.NoMatch):
            text = 'Print 1\nblah\nPrint unreachable'
            result = self.parse(text)
            assert False, 'arpeggio.NoMatch exception expected'


    def test_error02(self):
        """No instruction separator"""
        text = 'Nop Nop'
        with self.assertRaises(arpeggio.NoMatch):
            result = '[%s]' % self.parse(text)


    def test_grammar4c(self):
        """Select statement with Else"""
        text = 'Select a\nCase 1\nNop\nNop\nCase Else\nNop\nNop\nEnd Select'
        self.check_grammar(text, '[Select | a | \n | Case | 1 | \n | Nop | \n | Nop | \n | Case | Else | \n | Nop | \n | Nop | \n | End | Select | ]')


    def test_grammar4d(self):
        """Simple Do-loop example 2"""
        text = 'Select a\nCase Is > 3\nCls\n?"a > 3"\nEnd Select'
        self.check_grammar(text, """[Select | a | 
 | Case | Is | > | 3 | 
 | Cls | 
 | ? |  | " | a |   | > |   | 3 | " | 
 | End | Select | ]""")


    def test_grammar_error4(self):
        """Select statement with Else in the wrong place"""
        with self.assertRaises(arpeggio.NoMatch):
            text = 'Select a\nCase Else\nNop\nNop\nCase 1\nNop\nNop\nEnd Select'
            result = self.parse(text)


    def test_grammar5a(self):
        """Simplest Do-loop example 1"""
        text = 'Do\nLoop While a > 0'
        self.check_grammar(text, '[Do | \n | Loop | While | a | > | 0 | ]')


    def test_grammar5b(self):
        """Simplest Do-loop example 2"""
        text = 'Do While a > 0\nLoop'
        self.check_grammar(text, '[Do | While | a | > | 0 | \n | Loop | ]')


    def test_grammar5c(self):
        """Simple Do-loop example 1"""
        text = 'Do\nCls\n?"Processing..."\nLoop While a > 0'
        self.check_grammar(text, """[Do | 
 | Cls | 
 | ? |  | " | P | r | o | c | e | s | s | i | n | g | . | . | . | " | 
 | Loop | While | a | > | 0 | ]""")


    def test_grammar5d(self):
        """Simple Do-loop example 2"""
        text = 'Do While a > 0:\nCls\n?"Processing..."\nLoop'
        self.check_grammar(text, """[Do | While | a | > | 0 | : | 
 | Cls | 
 | ? |  | " | P | r | o | c | e | s | s | i | n | g | . | . | . | " | 
 | Loop | ]""")


    def test_grammar6a(self):
        """Simplest function example"""
        text = 'Function f() as String\nEnd Function'
        self.check_grammar(text, '[Function | f | ( | ) | As | String | \n | End | Function | ]')


    def test_grammar6b(self):
        """Simple function example"""
        text = 'Function f(s as String) as String\nf = "hello, world"\nExit Function\nEnd Function'
        self.check_grammar(text, '[Function | f | ( | s | As | String | ) | As | String | \n | f | = | " | h | e | l | l | o | , |   | w | o | r | l | d | " | \n | Exit | Function | \n | End | Function | ]')


    def test_grammar6c(self):
        """Simplest sub example"""
        text = 'Sub s()\nEnd Sub'
        self.check_grammar(text, '[Sub | s | ( | ) | \n | End | Sub | ]')


    def test_grammar6d(self):
        """Wrong sub declaration"""
        text = 'Sub s(s as String) as String\nEnd Function'
        with self.assertRaises(arpeggio.NoMatch):
            result = '[%s]' % self.parse(text)


    def test_grammar_in_files(self):
        test_files = glob(path.join('tests', 'samples', '*.asc'))
        test_files.sort()
        for filename in test_files:
            try:
                with open(filename, 'r') as source_file, open(path.splitext(filename)[0] + '.tree', 'r') as tree_file:
                    source_code, tree = source_file.read().strip(), tree_file.read().strip()
                    self.check_grammar(source_code, tree, filename)
            except FileNotFoundError as e:
                with open(filename, 'r') as source_file:
                    source_code = source_file.read().strip()
                    result = '[%s]' % self.parse(source_code)
                with open(path.splitext(filename)[0] + '.tree', 'w') as tree_file:
                    print(result, file=tree_file)

