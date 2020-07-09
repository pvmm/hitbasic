from contextlib import suppress
from arpeggio import ParseTreeNode, And, Sequence, Optional, ZeroOrMore, OneOrMore, EOF, RegExMatch as _, ParserPython


def create_var_parser(known_vars, **kwargs):
    try:
        debug_mode = kwargs['debug']
    except KeyError:
        debug_mode = False
    def var_name():         return And( known_vars_rule ), expr, EOF
    def expr():             return eqv_op, ZeroOrMore( _(r'Imp'), eqv_op )
    def expr_1p():          return ZeroOrMore( _(r'Imp'), eqv_op )
    def eqv_op():           return xor_op, ZeroOrMore( _(r'Eqv'), xor_op )
    def eqv_op_1p():        return ZeroOrMore( _(r'Eqv'), xor_op )
    def xor_op():           return or_op, ZeroOrMore( _(r'Xor'), or_op )
    def xor_op_1p():        return ZeroOrMore( _(r'Xor'), or_op )
    def or_op():            return and_op, ZeroOrMore( _(r'or'), and_op )
    def or_op_1p():         return ZeroOrMore( _(r'or'), and_op )
    def and_op():           return not_op, ZeroOrMore( _(r'And'), not_op )
    def and_op_1p():        return ZeroOrMore( _(r'And'), not_op )
    def not_op():           return ZeroOrMore( _(r'Not') ), comp_op
    def comp_op():          return add_op, ZeroOrMore( comptor, add_op )
    def case_comp_op():     return comptor, add_op
    def add_op():           return mod_op, ZeroOrMore( add_or_sub_tk, mod_op )
    def mod_op():           return idiv_op, ZeroOrMore( _(r'Mod'), idiv_op )
    def mod_op_1p():        return ZeroOrMore( _(r'Mod'), idiv_op )
    def idiv_op():          return mul_op, ZeroOrMore( _(r'\\'), mul_op )
    def mul_op():           return neg_op, ZeroOrMore( mul_or_div_tk, neg_op )
    def neg_op():           return ZeroOrMore( signal ), exp_op
    def exp_op():           return optor, ZeroOrMore( _('\^'), optor )
    def optor():            return [ ( '(', expr, ')' ), numeral, string, rvalue ]

    def rvalue():           return [ array, scalar ]
    def array():            return array_name, array_args
    def array_name():       return known_vars_rule, Optional( type_des )
    def array_args():       return '(', Optional( exprs ), ')'
    def exprs():            return expr, ZeroOrMore( ',', expr )
    def scalar():           return scalar_name
    def scalar_name():      return known_vars_rule, Optional( type_des )
    def numeral():          return [ fractional, integer ]
    def fractional():       return Optional( add_or_sub_tk ), Optional( digit ), '.', ZeroOrMore( digit )
    def integer():          return [ ( signal, OneOrMore( digit ) ),
                                     ( signal, hex_prefix, OneOrMore( hex_digit ) ),
                                     ( signal, oct_prefix, OneOrMore( oct_digit ) ),
                                     ( signal, bin_prefix, OneOrMore( bin_digit ) ) ]
    def digit():            return _(r'[0-9]')
    def hex_prefix():       return _(r'&H')
    def hex_digit():        return _(r'[0-9A-F]')
    def oct_prefix():       return _(r'&O')
    def oct_digit():        return _(r'[0-7]')
    def bin_prefix():       return _(r'&B')
    def bin_digit():        return _(r'[01]')
    def string():           return '"', Sequence( ZeroOrMore( non_quote_char ), skipws=False ), '"'
    def trailing_spaces():  return _(r'\s*')
    def reserved():         return [ 'And', 'As', 'Imp', 'Eqv', 'Mod', 'Or', 'Xor' ]
    #def alphanum_name():    return [ known_vars_rule, ZeroOrMore([ reserved, known_vars_rule ])]
    def alphanum_name():    return _(r'[A-Z][_A-Z0-9]*')
    def type_des():         return _(r'[#!%]?')
    def known_vars_rule():  return known_vars
    def comptor():          return [ '=', '<>', '<=', '<', '>=', '>']
    def non_quote_char():   return _(r'[^"]')
    def eq_tk():            return [ '=' ]
    def mul_or_div_tk():    return [ '*', '/' ]
    def signal():           return Optional( add_or_sub_tk )
    def add_or_sub_tk():    return [ '+', '-' ]
    def add_tk():           return [ '+' ]

    return ParserPython(var_name, reduce_tree=False, ignore_case=True, ws='\t ', skipws=True, debug=debug_mode)
