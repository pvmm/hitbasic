#!/bin/env python3

import re
import sys
import BASIC


# Options
force_declaration = True
generate_var_type = True
verbose = True


def debug(*args, **kargs):
    if verbose: print(*args, **kargs)


warn = print


class Variable:
    UNDECLARED = -1
    UNDEFINED = 0
    INTEGER = 1
    SINGLE = 2
    DOUBLE = 3
    STRING = 4
    RESERVED = 5
    FUNCTION = 6 # DEF FN
    default_type = DOUBLE
    types = [UNDEFINED, INTEGER, SINGLE, DOUBLE, STRING]
    type_char = {'%' : INTEGER, '!': SINGLE, '#': DOUBLE, '$': STRING}
    type_names = ['Undefined', 'Integer', 'Single', 'Double', 'String']

    @classmethod
    def check_type(klass, var, defn_type):
        '''Check if variable can receive a value based on each one's types.'''
        if var[-1:] in klass.type_char.keys():
            if generate_var_type:
                warn("HitBasic is configured to create variable types automatically so you don't need to specify variable type suffixes for your variables.")
                #warn(Context.location())
            decl_type = klass.types[klass.type_char[var[-1:]]]
        else:
            if not generate_var_type:
                decl_type = default_type
            else:
                return defn_type

        if decl_type != defn_type:
            raise Exception('Type mismatch between variable of type %s and value of type %s'
                    % (klass.type2str(decl_type), klass.type2str(defn_type)))
        else:
            return decl_type


    @classmethod
    def coerce_type(klass, type1, type2):
        '''Check if two variable types are compatible in cast/coerce operations.'''
        if type1 == type2:
            return type1

        _set = [type1, type2]

        if Variable.UNDECLARED in _set:
            if type1 == Variable.UNDECLARED:
                return type2
            return type1

        if Variable.UNDEFINED in _set:
            if type1 == Variable.UNDEFINED:
                return type2
            else:
                return type1

        if Variable.STRING in _set:
            raise Exception('Type mismatch')

        if Variable.SINGLE in _set:
            if Variable.DOUBLE in _set:
                return Variable.DOUBLE
            return Variable.SINGLE

        if Variable.INTEGER in _set:
            if Variable.SINGLE in _set:
                return Variable.SINGLE
            if Variable.DOUBLE in _set:
                return Variable.DOUBLE


    @classmethod
    def type2str(klass, type):
        '''string version of variable type'''
        return klass.type_names[type]


    def __init__(self, name, type, value=None):
        self.name = name
        self.type = type
        self.value = value


class Context(object):
    var_name = None
    var_type = Variable.UNDECLARED
    symbol_table = {
            # predefined BASIC variables. 
            'COLOR': Variable('COLOR', Variable.RESERVED),
            'ERL': Variable('ERL', Variable.RESERVED),
            'ERR': Variable('ERR', Variable.RESERVED),
            'INKEY$': Variable('INKEY$', Variable.RESERVED),
            'MAXFILES': Variable('MAXFILES', Variable.RESERVED),
            'TIME': Variable('TIME', Variable.RESERVED),
            'SPRITE$': Variable('SPRITE$', Variable.RESERVED)
    }
    reserved_words = ['CLS', 'FOR', 'IF']
    forloop_scope = []


    def check_var_name(self, var_name):
        for word in self.reserved_words:
            if var_name.upper().startswith(word):
                raise Exception('Syntax error')


    def mark_type_integer(self, text, start, end, elements):
        debug("mark_type_integer(%s)", Variable.type2str(Variable.INTEGER))
        self.var_type = Variable.coerce_type(self.var_type, Variable.INTEGER)


    def mark_type_single(self, text, start, end, elements):
        debug("mark_type_float(%s)", Variable.type2str(Variable.SINGLE))
        self.var_type = Variable.coerce_type(self.var_type, Variable.SINGLE)


    def mark_type_string(self, text, start, end, elements):
        debug("mark_type_string(%s)", Variable.type2str(Variable.STRING))
        self.var_type = Variable.coerce_type(self.var_type, Variable.STRING)


    def check_var_range(self, text, start, end, elements):
        debug("check_var_range(%s)" % text[start:end])
        if ord(text[start:start+1].upper()) > ord(text[end-1:end].upper()):
            # DEFINT Z-A is an example of invalid range.
            raise Exception('Variable range invalid')


    def store_val(self, text, start, end, elements):
        #self.var_value = elements
        self.var_value = text[start:end]


    def define_var(self, text, start, end, elements):
        '''Force user to declare a variable before defining it.'''
        self.check_var_name(text[start:end])
        if force_declaration:
            if not self.var_name.upper() in self.symbol_table.keys():
                raise Exception('Variable "%s" undeclared' % self.var_name)
        else:
            # force_declaration is off: definition is declaration
            self.symbol_table[self.var_name.upper()] = Variable(self.var_name, self.var_type)


    def declare_var(self, text, start, end, elements):
        '''Put a variable in the symbol table.'''
        self.var_type = Variable.check_type(self.var_name, self.var_type)
        if self.var_name.upper() in self.symbol_table.keys():
            raise Exception('Name already declared')
        self.symbol_table[self.var_name.upper()] = Variable(self.var_name, self.var_type, self.var_value)
        debug("* declare_var(%s as %s) = %s" % (self.var_name, Variable.type2str(self.var_type), self.var_value))
        # reset
        self.var_name, self.var_type, self.var_value  = None, Variable.UNDECLARED, None


    def push_forloop_var(self, text, start, end, elements):
        self.var_type = Variable.check_type(self.var_name, self.var_type)
        self.symbol_table[self.var_name.upper()] = Variable(self.var_name, self.var_type, self.var_value)
        self.forloop_scope.append(self.var_name)
        debug("* push_forloop_var(%s)" % self.var_name)
        # reset
        self.var_name, self.var_type, self.var_value  = None, Variable.UNDECLARED, None


    def pop_forloop_var(self, text, start, end, elements):
        var_name = self.forloop_scope[-1:][0]
        debug("* pop_forloop_var(%s, %s)" %(text[start:end], var_name))
        if text[start:end] != var_name:
            raise Exception("Next control variable does not match For loop control variable '%s'." % var_name)
        else:
            self.forloop_scope.pop()


    def pop_forloop(self, text, start, end):
        debug("* pop_forloop()")
        try:
            var_name = self.forloop_scope.pop()
        except IndexError:
            raise Exception("'Next' must be preceded by a matching 'For'")


    def store_var_name(self, text, start, end, elements):
        self.var_name = re.sub(r"\s*", "", text[start:end])


    def check_calc(self, text, start, end, elements):
        debug("calc = %s" % text[start:end])
        debug(elements)


    def check_logical(self, text, start, end, elements):
        debug("logical = %s" % text[start:end])
        debug(elements)


    def check_comparison(self, text, start, end, elements):
        debug("comparison = %s" % text[start:end])
        debug(elements)


    def check_addsub(self, text, start, end, elements):
        debug("addsub = %s" % text[start:end])
        debug(elements)


    def check_modulo(self, text, start, end, elements):
        debug("modulo = %s" % text[start:end])
        debug(elements)


    def check_intdiv(self, text, start, end, elements):
        debug("intdiv = %s" % text[start:end])
        debug(elements)


    def check_muldiv(self, text, start, end, elements):
        debug("muldiv = %s" % text[start:end])
        debug(elements)


    def check_neg(self, text, start, end, elements):
        debug("neg = %s" % text[start:end])
        debug(elements)


    def check_exp(self, text, start, end, elements):
        debug("exp = %s" % text[start:end])
        debug(elements)


    def check_overflow(self, s, base=10):
        '''Check if number is bigger than 16bit'''
        if int(s, base) > 65535:
            raise BASIC.ParserError('overflow')


    def check_overflow_hex(self, text, start, end, elements):
        '''Check if number is bigger than 16bit, hexadecimal edition'''
        s = elements[2].text.upper()
        self.check_overflow(s, 16)


    def check_overflow_oct(self, text, start, end, elements):
        '''Check if number is bigger than 16bit, octal edition'''
        s = elements[2].text.upper()
        self.check_overflow(s, 8)


    def check_overflow_bin(self, text, start, end, elements):
        '''Check if number is bigger than 16bit, binary edition'''
        s = elements[2].text.upper()
        self.check_overflow(s, 2)


text = ""

for line in sys.stdin:
    text += line

try:
    tree = BASIC.parse(text, actions=Context())

    for node in tree.elements:
        debug(node.offset, node.text)

except BASIC.ParseError as e:
    print('* Parse error::', str(e)[0].lower() + str(e)[1:])
    pass
