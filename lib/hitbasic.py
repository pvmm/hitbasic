from contextlib import suppress
from arpeggio import UnorderedGroup, Sequence, Optional, ZeroOrMore, OneOrMore, EOF, ParserPython, And, Not, Empty, RegExMatch as _
from arpeggio import ParseTreeNode


# Top tier
def program():          return trailing_spaces, [ Optional( statements ), EOF ], trailing_spaces, EOF
def statements():       return opt_stmt_sep, [ ( label_stmt, opt_stmt_sep, statement ), statement ], ZeroOrMore( statement_sep, statements )
def statement():        return [ function_stmt,
                                 sub_stmt,
                                 dim_stmt,
                                 if_then_else_stmt,
                                 select_stmt,
                                 do_loop_stmt,
                                 next_stmt,
                                 for_stmt,
                                 print_stmt,
                                 branch_stmts,
                                 exit_stmt,
                                 let_stmt,
                                 ( 'Def', range_type_decl ),
                                 input_stmt,
                                 graphics_stmts,
                                 play_stmt,
                                 paramless_stmt,
                                 #multi_attr_stmt,
                                 attr_stmt ]
def trailing_spaces():  return _(r'\s*')
def comments():         return [ comments1, comments2 ]
def comments1():        return [ _(r"\s*'[^\n]*"),
                                 ( _(r"^(Rem|')[^\n]*"), new_line ),
                                 ( ':', _(r"\s*(Rem|')[^\n]*") ) ]
def comments2():        return [ ( _(r"^\s*'[^\n]*"), new_line ),
                                 ( _(r"^\s*(Rem|')[^\n]*"), new_line ),
                                 ( ':', _(r"(Rem|')[^\n]*"), new_line ) ]


# Dim rules
def dim_stmt():         return 'Dim', dim_vars
def dim_vars():         return dim_var_decl, ZeroOrMore( ',', dim_var_decl )
def dim_var_decl():     return [ ( dim_var, dim_as_kw, dim_var_type, dim_eq_tk, dim_init ),
                                 ( dim_var, dim_as_kw, dim_var_type ),
                                 ( dim_var, dim_eq_tk, dim_init ),
                                   dim_var ]
def dim_var_type():     return var_type
def dim_var():          return dim_var_name, Optional( _('\('), dim_var_ranges, _('\)') )
def dim_var_ranges():   return Optional( dim_var_expr, ZeroOrMore( _(r','), dim_var_expr ) )
def dim_var_name():     return alphanum_name, Optional( type_des )
def dim_var_expr():     return ZeroOrMore( [ ( num_expr, 'To', num_expr ), ( num_expr, ) ] )
def dim_init():         return [ ( '{', Optional( dim_init_array ), '}' ), expr ]
def dim_init_array():   return dim_init, ZeroOrMore( ',', dim_init )
def dim_as_kw():        return 'As'
def dim_eq_tk():        return '='


# If-then-else rules
def if_then_else_stmt():  return [
                        ( 'If', expr, 'Then', Optional( statement_sep ), Optional( then_clauses ), Optional( statement_sep ), 'Else', Optional( statement_sep ), Optional( else_clauses ), Optional( statement_sep ), end_if_stmt ),
                        ( 'If', expr, 'Then', Optional( statement_sep ), Optional( else_clauses, statement_sep ), end_if_stmt ),
                        ( 'If', expr, 'Then', inln_then_clauses, 'Else', inln_else_clauses ),
                        ( 'If', expr, 'Then', inln_else_clauses ),
                        ( 'If', expr, 'Goto', label_clause, 'Else', label_clause ),
                        ( 'If', expr, 'Goto', label_clause )
                        ]
def inln_then_clauses():  return Optional( inln_stmts ), And( 'Else' )
def inln_else_clauses():  return Optional( inln_stmts ), And([ EOF, new_line ])
def inln_stmts():         return statement, ZeroOrMore( ':', inln_stmts )
def then_clauses():       return [ ( label_stmt, statement ), statement ], ZeroOrMore( statement_sep, then_clauses ), And([ statement_sep, 'Else' ])
def else_clauses():       return [ ( label_stmt, statement ), statement ], ZeroOrMore( statement_sep, else_clauses ), And([( statement_sep, end_if_stmt ), end_if_stmt ])
def end_if_stmt():        return 'End', 'If'


# Select rules
def select_stmt():      return 'Select', expr, statement_sep, ZeroOrMore( select_case, new_line ), Optional( select_case_else, new_line ), 'End', 'Select'
def select_case():      return 'Case', case_exprs, statement_sep, Optional( case_block ), end_case_block #, new_line
def select_case_else(): return 'Case', 'Else', statement_sep, Optional( case_block ), end_case_block #, new_line
def case_block():       return Not([ ( 'End', 'Select' ), 'Case' ]), [ ( label_stmt, statement ), statement ], ZeroOrMore( statement_sep, case_block )
def end_case_block():   return And( new_line, [ ( 'End', 'Select' ), 'Case' ] )
#def end_case_block():   return And( [ ( 'End', 'Select' ), 'Case' ] )
#def end_case_block():   return And( Optional( new_line ), [ ( 'End', 'Select' ), 'Case' ] )
def case_exprs():       return [ case_comparison, case_interval, case_value ], ZeroOrMore( ',', case_exprs )
def case_comparison():  return [ 'Is', '' ], case_comp_op
def case_interval():    return case_intvl_value, 'To', case_intvl_value
def case_intvl_value(): return Not( 'To' ), expr # Any expr but the keyword 'To'
def case_value():       return Not( 'Else' ), expr # Any expr but the keyword 'Else'


# Def<Type> rules
def range_type_decl():  return var_type, var_ranges
def var_type():         return [ 'Boolean', 'BOOL', 'Integer', 'INT', 'String', 'STR', 'Single', 'SNG', 'Double', 'DBL' ]
def var_ranges():       return var_range, ZeroOrMore( ',', var_range )
def var_range():        return _(r'[A-Z]'), '-', _(r'[A-Z]')


# DoLoop rules
def do_loop_stmt():     return [ ( 'Do', do_loop_cond, statement_sep, Optional( do_stmt_block, statement_sep ), 'Loop' ), # Loop in the beginning
                                 ( 'Do', opt_stmt_sep, Optional( do_stmt_block, opt_stmt_sep ), 'Loop', do_loop_cond ) ]  # Loop in the end
def do_loop_cond():     return [ 'While', 'Until' ], expr
def do_stmt_block():    return [ ( label_stmt, do_stmt ), do_stmt ], ZeroOrMore( statement_sep, do_stmt_block ), And( statement_sep, 'Loop' )
def do_stmt():          return [ ( 'Exit', 'Do' ), statement ]


# For loop rules
def for_stmt():         return 'For', var, '=', for_range_decl
def for_range_decl():   return [ ( num_expr, 'To', num_expr, 'Step', num_expr ), ( num_expr, 'To', num_expr ) ]
def next_stmt():        return 'Next', next_vars
def next_vars():        return next_var, ZeroOrMore( ',', next_var )
def next_var():         return var


# Function rules
def function_stmt():    return [ func_head1, func_head2 ], statement_sep, Optional( func_body, statement_sep ), func_end_stmt
def func_head1():       return 'Function', alphanum_name, '(', Optional( func_vars ), ')', func_return_type
def func_head2():       return 'Function', alphanum_name, Optional( type_des ), '(', Optional( func_vars ), ')'
def func_vars():        return func_var_decl, ZeroOrMore( ',', func_var_decl )
def func_return_type(): return 'As', var_type
def func_var_decl():    return [ ( alphanum_name, 'As', var_type ),
                                 ( alphanum_name, Optional( type_des ) ) ]
def func_body():        return [ ( label_stmt, func_body_stmt ), func_body_stmt ], ZeroOrMore( statement_sep, func_body ), And( statement_sep, func_end_stmt )
def func_exit_stmt():   return 'Exit', 'Function'
def func_body_stmt():   return [ func_exit_stmt, statement ]
def func_end_stmt():    return 'End', 'Function'


# Sub rules
def sub_stmt():         return 'Sub', alphanum_name, '(', Optional( sub_vars ), ')', statement_sep, Optional( sub_body, statement_sep ), sub_end
def sub_vars():         return sub_var_decl, ZeroOrMore( ',', sub_var_decl )
def sub_var_decl():     return [ ( alphanum_name, 'As', var_type ), ( alphanum_name, Optional( type_des ) ) ]
def sub_body_stmt():    return [ ( 'Exit', 'Sub' ), statement ]
def sub_body():         return [ ( label_stmt, sub_body_stmt ), sub_body_stmt ], ZeroOrMore( statement_sep, sub_body ), And( statement_sep, sub_end )
def sub_end():          return 'End', 'Sub'


# Input rules
def input_stmt():       return 'Input', [ input_prompt, input_file ]
def input_prompt():     return ( Optional( string, ';' ), input_vars )
def input_file():       return ( '#', num_expr, ',', input_vars )
def input_vars():       return var, ZeroOrMore( ',', var )


# Print rules
def print_stmt():       return [ '?', 'Print' ], [ print_fileno, '' ], Optional( print_params )
def print_params():     return [ [ print_using_fmt, print_exprs ],
                                 ( print_exprs, print_using_fmt ) ]
def print_fileno():     return '#', num_expr, ','
def print_using_fmt():  return 'Using', [ string, var], ';', print_exprs
def print_exprs():      return print_expr, ZeroOrMore( print_sep, print_expr )
def print_expr():       return Not( 'Using' ), expr # Any expr but the keyword 'Using'
def print_sep():        return [ ',', ';' ]


# branch instructions
def branch_stmts():     return [ on_sprite_stmt, on_interval_stmt, on_branch_stmt, branch_stmt, return_stmt ]
def on_sprite_stmt():   return 'On', 'Sprite', 'Gosub', numeral
def on_interval_stmt(): return 'On', ( interval_tk, eq_tk, num_expr ), 'Gosub', comma_sep_adrs
def on_branch_stmt():   return 'On', num_expr, branch_tk, comma_sep_adrs
def branch_stmt():      return branch_tk, [ label_clause, numeral ]
def return_stmt():      return 'Return', Optional([ label_clause, numeral ])
def comma_sep_adrs():   return ZeroOrMore(',', numerals )
def comma_sep_adrs():   return Optional([ label_clause, numeral ]), ZeroOrMore( comma, Optional([ label_clause, numeral ]) )
def branch_tk():        return [ goto_tk, gosub_tk ]
def goto_tk():          return [ 'Goto' ]
def gosub_tk():         return [ 'Gosub' ]


# label stmt
def label_stmt():       return label_addr, Optional( label_stmt )
def label_addr():       return '@', _(r'[_A-Z][_A-Z0-9]*'), Optional(':') # some BASIC dialects require the ending ':'
def label_clause():     return _(r'[_A-Z][_A-Z0-9]*')
#def label():            return '@', _(r'[_A-Z][_A-Z0-9]*')


# branch related statements
def switcher_stmt():    return switchers_tk, switch_tk
def swichers_tk():      return [ interval_tk, sprite_tk ]
def switch_tk():        return [ 'On', 'Off', 'Stop' ]
def interval_tk():      return [ 'Interval' ]
def sprite_tk():        return [ 'Sprite' ]


# Exit rules
def exit_stmt():        return 'Exit', [ 'Function', 'Sub' ]

# Graphics statements
def graphics_stmts():   return [ draw_stmt, circle_stmt, color_stmt, copy_stmt, line_stmt, paint_stmt, preset_stmt,
                                 pset_stmt, put_sprite_stmt, screen_stmt ]
def draw_stmt():        return 'Draw', str_expr
def circle_stmt():      return 'Circle', g_ostep_point, circle_stmt_args
def circle_stmt_args(): return Optional( comma, g_color, Optional( comma, g_color ) )
def color_stmt():       return 'Color', Optional( g_color ), Optional( comma, g_color, Optional( comma, g_color ) )
def copy_stmt():        return 'Copy', g_copy_src, 'To', g_copy_dst
def line_stmt():        return 'Line', Optional( g_ostep_point ), g_dst_ostep_point, line_stmt_args
def line_stmt_args():   return Optional( comma, g_color, Optional( comma, g_shape, Optional( comma, g_optor ) ) )
def paint_stmt():       return 'Paint', g_ostep_point, paint_stmt_args
def paint_stmt_args():  return Optional( comma, g_color, Optional( comma, g_color ) )
def preset_stmt():      return 'Preset', g_ostep_point, preset_stmt_args
def preset_stmt_args(): return Optional( comma, g_color, Optional( comma, g_optor ) )
def pset_stmt():        return 'Pset', g_ostep_point, pset_stmt_args
def pset_stmt_args():   return Optional( comma, g_color, Optional( comma, g_optor ) )
def put_sprite_stmt():  return 'Put', 'Sprite', num_expr, comma, g_ostep_point, put_sprite_stmt_args
def put_sprite_stmt_args(): return Optional( comma, g_color, Optional( comma, g_pttn_num ) )
def screen_stmt():      return 'Screen', Optional( g_mode ), Optional( comma ), Optional( g_sprite_size ), Optional( comma ), Optional( g_key_click ), Optional( comma ), Optional( g_baud_rate ), Optional( comma ), Optional( g_printer_type ), Optional( comma ), Optional( g_interlace_mode )

def g_radius():         return num_expr
def g_color():          return num_expr
def g_tracing_start():  return num_expr
def g_tracing_end():    return num_expr
def g_aspect():         return num_expr
def g_shape():          return [ 'BF', 'B' ]
def g_optor():          return [ 'And', 'Or', 'Preset', 'Pset', 'Xor', 'Tand', 'Tor', 'Tpreset', 'Tpset', 'Txor' ]
def g_page():           return num_expr
def g_mode():           return num_expr
def g_sprite_size():    return num_expr
def g_key_click():      return num_expr
def g_baud_rate():      return num_expr
def g_printer_type():   return num_expr
def g_interlace_mode(): return num_expr
def g_direction():      return num_expr
def g_pttn_num():       return num_expr
def g_dst_ostep_point():return _('-'), Optional( _( 'Step' ) ), g_point
def g_ostep_point():    return Optional( _( 'Step' ) ), g_point
def g_point():          return '(', num_expr, comma, num_expr, ')'
def g_copy_src():       return [ ( g_point, g_dst_ostep_point, Optional( comma, g_page ) ),
                                 ( g_array, Optional( comma, g_direction ) ),
                                 ( filepath, Optional( comma, g_direction ) ) ]
def g_copy_dst():       return [ ( g_point, Optional( comma, g_page, Optional( comma, g_optor ) ) ),
                                 ( filepath ),
                                 ( g_array ) ]
def g_array():          return alphanum_name, Optional( type_des )

# Play instruction
def play_stmt():        return 'Play', Optional( '#', num_expr, ',' ), Optional( str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr, Optional( ',', str_expr ) ) ) ) ) ) ) ) ) ) ) ) )


# Resume instruction
def resume_stmt():      return 'Resume', [ next_tk, numeral ]
def next_tk():          return 'Next'


# Instruction that accepts comma-separated lists.
def comma_lst_stmt():   return comma_lst_st_tk
def comma_lst_st_tk():  return [ 'Erase' ]


# Instruction with no parameters
def paramless_stmt():   return [ 'Nop', 'Cls', 'End' ]


# Single param instruction
def simple_stmt():      return simple_stmt_tk, num_expr
def simple_stmt_tk():   return [ 'Error', 'Width' ]


# Multi-attribution
def multi_attr_stmt():  return var_defns
def var_defns():        return lvalues, '=', exprs
def lvalues():          return var, ZeroOrMore( ',', var )


# Let and regular attribution rules
def let_stmt():         return 'Let', var_defn
def attr_stmt():        return var_defn
def var_defn():         return var, '=', expr


# expr rules
def expr():             return eqv_op, ZeroOrMore( _(r'Imp'), eqv_op )
def eqv_op():           return xor_op, ZeroOrMore( _(r'Eqv'), xor_op )
def xor_op():           return or_op, ZeroOrMore( _(r'Xor'), or_op )
def or_op():            return and_op, ZeroOrMore( _(r'or'), and_op )
def and_op():           return not_op, ZeroOrMore( _(r'And'), not_op )
def not_op():           return ZeroOrMore( _(r'Not') ), comp_op
def comp_op():          return add_op, ZeroOrMore( comptor, add_op )
def case_comp_op():     return comptor, add_op
def add_op():           return mod_op, ZeroOrMore( add_or_sub_tk, mod_op )
def mod_op():           return idiv_op, ZeroOrMore( _(r'Mod'), idiv_op )
def idiv_op():          return mul_op, ZeroOrMore( _(r'\\'), mul_op )
def mul_op():           return neg_op, ZeroOrMore( mul_or_div_tk, neg_op )
def neg_op():           return ZeroOrMore( signal ), exp_op
def exp_op():           return optor, ZeroOrMore( _('\^'), optor )
def optor():            return [ ( '(', expr, ')' ), numeral, string, var ]


# num_expr rules
def num_expr():         return num_imp_op
def num_imp_op():       return num_eqv_op, ZeroOrMore( 'Imp', num_eqv_op )
def num_eqv_op():       return num_xor_op, ZeroOrMore( 'Eqv', num_xor_op )
def num_xor_op():       return num_or_op, ZeroOrMore( 'Xor', num_or_op )
def num_or_op():        return num_and_op, ZeroOrMore( 'or', num_and_op )
def num_and_op():       return num_not_op, ZeroOrMore( 'And', num_not_op )
def num_not_op():       return ZeroOrMore( 'Not' ), num_comp_op
def num_comp_op():      return num_add_op, ZeroOrMore( comptor, num_add_op )
def num_case_comp_op(): return num_comptor, num_add_op
def num_add_op():       return num_mod_op, ZeroOrMore( add_or_sub_tk, num_mod_op )
def num_mod_op():       return num_idiv_op, ZeroOrMore( 'Mod', num_idiv_op )
def num_idiv_op():      return num_mul_op, ZeroOrMore( '\\', num_mul_op )
def num_mul_op():       return num_neg_op, ZeroOrMore( mul_or_div_tk, num_neg_op )
def num_neg_op():       return ZeroOrMore( signal ), num_exp_op
def num_exp_op():       return num_optor, ZeroOrMore( '^', num_optor )
def num_optor():        return [ ( '(', num_expr, ')' ), ( numeral, ), ( num_var, ) ]


# str_expr rules
def str_expr():         return str_comp_op
def str_comp_op():      return str_add_op, ZeroOrMore( comptor, str_add_op )
def str_add_op():       return str_optor, ZeroOrMore( add_tk, str_optor )
def str_optor():        return [ ( '(', str_expr, ')' ), ( string, ), ( str_var, ) ]


# General
def exprs():            return expr, ZeroOrMore( ',', expr )

def var():              return [ array, scalar ]
def array():            return array_name, array_args
def array_name():       return alphanum_name, Optional( type_des )
def array_args():       return '(', Optional( exprs ), ')'
def scalar():           return scalar_name
def scalar_name():      return alphanum_name, Optional( type_des )

def str_var():          return [ str_array, str_scalar ]
def str_array():        return str_array_name, array_args
def str_array_name():   return alphanum_name, Optional( str_type_des )
def str_scalar():       return str_scalar_name
def str_scalar_name():  return alphanum_name, Optional( str_type_des )

def num_var():          return [ num_array, num_scalar ]
def num_array():        return num_array_name, array_args
def num_array_name():   return alphanum_name, Optional( num_type_des )
def num_scalar():       return num_scalar_name
def num_scalar_name():  return alphanum_name, Optional( num_type_des )

def comptor():          return [ '=', '<>', '<=', '<', '>=', '>']
def non_quote_char():   return _(r'[^"]')
def any_char():         return _(r'[^\n]')
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
def filepath():         return string
def string():           return '"', Sequence( ZeroOrMore( non_quote_char ), skipws=False ), '"'
def opt_stmt_sep():     return Optional( statement_sep )
def statement_sep():    return [ ( new_lines, ':', new_lines ), OneOrMore( new_line ) ]
def signal():           return Optional( add_or_sub_tk )
def reserved():         return [ 'And', 'As', 'Imp', 'Eqv', 'Mod', 'Xor', 'Or' ] # 'To' and others?
# Mimics MSX-BASIC parsing rules by parsing "aimpb" as "A IMP B"
#def alphanum_name():    return Not( reserved ), _(r'[A-Z]'), ZeroOrMore( Not( reserved ), _(r'[A-Z0-9]') )
def alphanum_name():    return _(r'[A-Z][_A-Z0-9]*')
def num_type_des():     return _(r'[#!%]?')
def str_type_des():     return _(r'[$]?')
def type_des():         return _(r'[$#!%]')
def comma():            return _(',')
def new_lines():        return ZeroOrMore('\n')
def new_line():         return '\n'


# Useful token groups
def eq_tk():            return [ '=' ]
def mul_or_div_tk():    return [ '*', '/' ]
def add_or_sub_tk():    return [ '+', '-' ]
def add_tk():           return [ '+' ]


class Surrogate(ParseTreeNode):
    "surrogate objects create a more simple and direct representation of destination language's structures"

    def __init__(self, rule, position, error, **kwargs):
        super().__init__(rule, position, error)
        for key, value in kwargs.items():
            setattr(self, key, value)


    def translate(self):
        raise NotImplemented()


def create_parser(**kwargs):
    try:
        debug_mode = kwargs['debug']
    except KeyError:
        debug_mode = False

    return ParserPython(program, comments, reduce_tree=False, ignore_case=True, ws='\t ', skipws=True, debug=debug_mode)
