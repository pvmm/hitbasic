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


    def check_grammar(self, text, expected, msg=None):
        result = '[%s]' % self.parse(text)
        try:
            assert result == expected
        except AssertionError:
            result = '[%s]' % self.parse(text)
            print('\n', result)
        if msg:
            assert result == expected, msg
        else:
            assert result == expected, "parse tree result:\n" + result


    def test_empty(self):
        """An empty program is a valid program"""
        result = '[%s]' % self.parse('')
        assert result == '[ | ]'
        #self.assertEqual(result, '[ | ]')


    def test_grammar_0(self):
        """Parameterless Print"""
        text = """Print"""
        result = '[%s]' % self.parse(text)
        assert result == '[Print |  | ]'


    def test_grammar_1a(self):
        text = """Print 1"""
        tree = self.parse(text)
        result = '[%s]' % self.parse(text)
        assert result == '[Print |  | 1 | ]'


    def test_grammar1b(self):
        """Testing instructions serially"""
        text = """Print 1\nPrint 2\nEnd"""
        tree = self.parse(text)
        result = '[%s]' % self.parse(text)
        assert result == '[Print |  | 1 | \n | Print |  | 2 | \n | End | ]'


    def test_grammar1c(self):
        """Multiparametered Print"""
        text = """Print 1;2,3"""
        result = '[%s]' % self.parse(text)
        assert result == '[Print |  | 1 | ; | 2 | , | 3 | ]'


    def test_grammar1d(self):
        """MSX-BASIC style instruction separator"""
        text = """Print 1:Print 2"""
        result = '[%s]' % self.parse(text)
        assert result == '[Print |  | 1 | : | Print |  | 2 | ]'


    def test_grammar1e(self):
        """A simple expression test"""
        text = """Print 1 - 2 * 3 ^ 4 / 5 Mod 3 Imp 4 Eqv 5 <> 6"""
        result = '[%s]' % self.parse(text)
        assert result == '[Print |  | 1 | - | 2 | * | 3 | ^ | 4 | / | 5 | Mod | 3 | Imp | 4 | Eqv | 5 | <> | 6 | ]'
        #assert result == '[Print |  | 1 |  | - |  | 2 |  | * |  | 3 |  | ^ |  | 4 |  | / |  | 5 |  | Mod |  | 3 |  | Imp |  | 4 |  | Eqv |  | 5 |  | <> |  | 6 | ]'


    def test_grammar1f(self):
        """Obligatory string"""
        text = 'Print "Hello, world!"'
        result = '[%s]' % self.parse(text)
        assert result == '[Print |  | " | H | e | l | l | o | , |   | w | o | r | l | d | ! | " | ]'


    def test_grammar1g(self):
        text = 'Print "Hello, world!":Print var'
        result = '[%s]' % self.parse(text)
        assert result == '[Print |  | " | H | e | l | l | o | , |   | w | o | r | l | d | ! | " | : | Print |  | var | ]'


    def test_grammar1h(self):
        text = 'Print "Hello, world!"\nPrint var'
        result = '[%s]' % self.parse(text)
        assert result == '[Print |  | " | H | e | l | l | o | , |   | w | o | r | l | d | ! | " | \n | Print |  | var | ]'


    def test_grammar_error1(self):
        """Invalid instruction between Prints"""
        with suppress(arpeggio.NoMatch):
            text = 'Print 1\nBlah\nPrint unreachable'
            result = self.parse(text)
            assert False, 'arpeggio.NoMatch exception expected'


    def test_grammar2a(self):
        """Simple, single-line If-Then with empty Then-block"""
        text = 'If var = 1 Then\nNop'
        result = '[%s]' % self.parse(text)
        self.check_grammar(text, '[If | var | = | 1 | Then | \n | Nop | ]')
        #self.check_grammar(text, '[If |  | var | = | 1 |  | Then | \n | Nop | ]')


    def test_grammar2b(self):
        """Simple, single-line If-Then-Else with empty Else-block"""
        text = 'If var = 1 Then Else\nNop'
        self.check_grammar(text, '[If | var | = | 1 | Then | Else | \n | Nop | ]')


    def test_grammar2c(self):
        """Simple, single-line If-Then"""
        text = 'If var = 1 Then Print "var is 1"\nNop'
        self.check_grammar(text, '[If | var | = | 1 | Then | Print |  | " | v | a | r |   | i | s |   | 1 | " | \n | Nop | ]')
        #self.check_grammar(text, '[If | var | = | 1 | Then | Print | " | v | a | r |   | i | s |   | 1 | " | \n | Nop | ]')


    def test_grammar2d(self):
        """Single-line If-Then-Else with blocks"""
        text = 'If var = 1 Then Cls:?"1" Else Cls:?"not 1":End\nNop'
        self.check_grammar(text, '[If | var | = | 1 | Then | Cls | : | ? |  | " | 1 | " | Else | Cls | : | ? |  | " | n | o | t |   | 1 | " | : | End | \n | Nop | ]')
        #self.check_grammar(text, '[If | var | = | 1 | Then | Cls | : | ? | " | 1 | " | Else | Cls | : | ? | " | n | o | t |   | 1 | " | : | End | \n | Nop | ]')


    def test_grammar2e(self):
        """Multiline If-Then-Else with inner End statement"""
        text = 'If var = 1 Then\nCls\n?"1" Else\nCls\n?"done!"\nEnd\nEnd If'
        self.check_grammar(text, '[If | var | = | 1 | Then | \n | Cls | \n | ? |  | " | 1 | " | Else | \n | Cls | \n | ? |  | " | d | o | n | e | ! | " | \n | End | \n | End | If | ]')


    def test_grammar2f(self):
        """Multiline If-Then-Else statement with single line Then Block"""
        text = 'If var = 1 Then Cls\n?"1" Else\nCls\n?"done!"\nEnd\nEnd If'
        self.check_grammar(text, '[If | var | = | 1 | Then | Cls | \n | ? |  | " | 1 | " | Else | \n | Cls | \n | ? |  | " | d | o | n | e | ! | " | \n | End | \n | End | If | ]')


    def test_grammar2g(self):
        """Multiline If-Then-Else statement with single line Then Block"""
        text = 'If var = 1 Then Cls\n?"1"\nElse\nCls\n?"done!"\nEnd\nEnd If'
        self.check_grammar(text, '[If | var | = | 1 | Then | Cls | \n | ? |  | " | 1 | " | \n | Else | \n | Cls | \n | ? |  | " | d | o | n | e | ! | " | \n | End | \n | End | If | ]')


    def test_grammar2h(self):
        """Multiline If-Then-Else statement with single line Then Block"""
        text = 'If var = 1 Then\nCls\n?"1"\nElse\nCls\n?"done!"\nEnd\nEnd If'
        self.check_grammar(text, '[If | var | = | 1 | Then | \n | Cls | \n | ? |  | " | 1 | " | \n | Else | \n | Cls | \n | ? |  | " | d | o | n | e | ! | " | \n | End | \n | End | If | ]')


    def test_grammar2i(self):
        """Multiline If-Then-Else statement with single line Then Block"""
        text = 'If var = 1 Then Cls:?"1" Else\nCls\n?"done!"\nEnd\nEnd If'
        self.check_grammar(text, '[If | var | = | 1 | Then | Cls | : | ? |  | " | 1 | " | Else | \n | Cls | \n | ? |  | " | d | o | n | e | ! | " | \n | End | \n | End | If | ]')


    def test_grammar2j(self):
        text = """If var = 1 Then\nEnd If"""
        self.check_grammar(text, '[If | var | = | 1 | Then | \n | End | If | ]')


    def test_grammar2k(self):
        text = 'If var = 1 Then\n?"var is one"\nEnd If'
        self.check_grammar(text, '[If | var | = | 1 | Then | \n | ? |  | " | v | a | r |   | i | s |   | o | n | e | " | \n | End | If | ]')


    def test_grammar2l(self):
        text = 'If var = 1 Then\n?"one"\nElse\n?"not one"\nEnd If'
        self.check_grammar(text, '[If | var | = | 1 | Then | \n | ? |  | " | o | n | e | " | \n | Else | \n | ? |  | " | n | o | t |   | o | n | e | " | \n | End | If | ]')


    def test_grammar3a(self):
        """Simple For-Loop example"""
        text = """For i = 1 to 20\nPrint "a"\nPrint i\nInput a\nNext i"""
        self.check_grammar(text, '[For | i | = | 1 | To | 2 | 0 | \n | Print |  | " | a | " | \n | Print |  | i | \n | Input | a | \n | Next | i | ]')


    def test_grammar3b(self):
        text = 'For i = 1 to 20\n?i\nIf i = 1 Then ?i + 1\n?var\nNext i'
        self.check_grammar(text, """[For | i | = | 1 | To | 2 | 0 | 
 | ? |  | i | 
 | If | i | = | 1 | Then | ? |  | i | + | 1 | 
 | ? |  | var | 
 | Next | i | ]""")


    def test_grammar3c(self):
        text = 'For i = 1 to 20\n? i\nIf i = 1 Then Next i\n? i+1\nNext'
        self.check_grammar(text, """[For | i | = | 1 | To | 2 | 0 | 
 | ? |  | i | 
 | If | i | = | 1 | Then | Next | i | 
 | ? |  | i | + | 1 | 
 | Next | ]""")


    def test_grammar3d(self):
        """For-loop nested If clause with multiple Nexts"""
        text = 'For i = 1 to 20\nPrint i\nIf i = 1 Then Next\nPrint i + 1\nNext i'
        self.check_grammar(text, """[For | i | = | 1 | To | 2 | 0 | 
 | Print |  | i | 
 | If | i | = | 1 | Then | Next | 
 | Print |  | i | + | 1 | 
 | Next | i | ]""")


    def test_grammar_error3(self):
        """No instruction separator"""
        text = 'Nop Nop'
        with self.assertRaises(arpeggio.NoMatch):
            result = '[%s]' % self.parse(text)


    def test_grammar3e(self):
        """Nested For-loops"""
        text = 'For i = 1 to 20\nFor j = 1 to 20\n? i, j\nNext j, i'
        self.check_grammar(text, """[For | i | = | 1 | To | 2 | 0 | 
 | For | j | = | 1 | To | 2 | 0 | 
 | ? |  | i | , | j | 
 | Next | j | , | i | ]""")


    def test_grammar4a(self):
        """Simplest Select statement possible"""
        text = 'Select a\nEnd Select'
        self.check_grammar(text, '[Select | a | \n | End | Select | ]')


    def test_grammar4b(self):
        """Two-Cases Select statement"""
        text = 'Select a\nCase 1\nNop\nNop\nCase 2\nNop\nNop\nEnd Select'
        self.check_grammar(text, '[Select | a | \n | Case | 1 | \n | Nop | \n | Nop | \n | Case | 2 | \n | Nop | \n | Nop | \n | End | Select | ]')


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
        for file in test_files:
            print('Reading file "%s"' % file)
            try:
                with open(file, 'r') as basic_file, open(path.splitext(file)[0] + '.tree', 'r') as tree_file:
                    text, tree = basic_file.read().strip(), tree_file.read().strip()
                    self.check_grammar(text, tree, "error on file %s" % file)
            except IOError as e:
                with open(file, 'r') as basic_file, open(path.splitext(file)[0] + '.tree', 'w') as tree_file:
                    text = basic_file.read()
                    result = '[%s]' % self.parse(text)
                    print(result, file=tree_file)

