from contextlib import suppress
from arpeggio import UnorderedGroup, Sequence, Optional, ZeroOrMore, OneOrMore, EOF, ParserPython, And, Not, Empty, RegExMatch as RegEx
from arpeggio import ParseTreeNode


# Top tier
def program():          return trailing_spaces, Optional( statements ), trailing_spaces, EOF
def statements():       return opt_stmt_sep, [ ( label_stmt, opt_stmt_sep, statement ), statement, label_stmt ], ZeroOrMore( statement_sep, statements )
def statement():        return [ function_stmt,
                                 sub_stmt,
                                 dim_stmt,
                                 if_then_else_stmt,
                                 select_stmt,
                                 do_loop_stmt,
                                 close_stmt,
                                 [ open_stmt, open_stmt_rnd ],
                                 next_stmt,
                                 for_stmt,
                                 print_stmt,
                                 branch_stmts,
                                 exit_stmt,
                                 graphics_stmts,
                                 let_stmt,
                                 ( 'Def', range_type_decl ),
                                 input_stmt,
                                 play_stmt,
                                 switcher_stmt,
                                 paramless_stmt,
                                 #multi_attr_stmt,
                                 attr_stmt ]
def trailing_spaces():  return RegEx(r'\s*')
def comments():         return [ "'" , 'Rem' ], ZeroOrMore( Not("\n"), RegEx('.') ), And([ new_line, EOF ])

# Dim rules
def dim_stmt():         return 'Dim', dim_vars
def dim_vars():         return dim_var_decl, ZeroOrMore( ',', dim_var_decl )
def dim_var_decl():     return [ ( dim_var, dim_as_kw, dim_var_type, dim_eq_tk, dim_init ),
                                 ( dim_var, dim_as_kw, dim_var_type ),
                                 ( dim_var, dim_eq_tk, dim_init ),
                                   dim_var ]
def dim_var_type():     return var_type
def dim_var():          return dim_var_name, Optional( RegEx('\('), dim_var_ranges, RegEx('\)') )
def dim_var_ranges():   return Optional( dim_var_expr, ZeroOrMore( RegEx(r','), dim_var_expr ) )
def dim_var_name():     return alphanum_name, Optional( type_des )
def dim_var_expr():     return ZeroOrMore( [ ( expr, 'To', expr ), ( expr, ) ] )
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
def select_stmt():      return 'Select', expr, statement_sep, ZeroOrMore( select_case ), Optional( select_case_else, new_line ), 'End', 'Select'
def select_case():      return 'Case', case_exprs, statement_sep, Optional( case_block ), end_case_block #, new_line
def select_case_else(): return 'Case', 'Else', statement_sep, Optional( case_block ), end_case_block #, new_line
def case_block():       return Not([ ( 'End', 'Select' ), 'Case' ]), [ ( label_stmt, statement ), statement ], ZeroOrMore( statement_sep, case_block )
def end_case_block():   return new_line, And( [ ( 'End', 'Select' ), 'Case' ] )
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
def var_range():        return RegEx(r'[A-Z]'), '-', RegEx(r'[A-Z]')


# DoLoop rules
def do_loop_stmt():     return [ ( 'Do', do_loop_cond, statement_sep, Optional( do_stmt_block, statement_sep ), 'Loop' ), # Loop in the beginning
                                 ( 'Do', opt_stmt_sep, Optional( do_stmt_block, opt_stmt_sep ), 'Loop', do_loop_cond ) ]  # Loop in the end
def do_loop_cond():     return [ 'While', 'Until' ], expr
def do_stmt_block():    return [ ( label_stmt, do_stmt ), do_stmt ], ZeroOrMore( statement_sep, do_stmt_block ), And( statement_sep, 'Loop' )
def do_stmt():          return [ ( 'Exit', 'Do' ), statement ]


# Open statement
def open_stmt_rnd():    return 'Open', filepath, 'As', file_fileno, Optional( 'Len', '=', expr )
def open_stmt():        return 'Open', filepath, 'For', ['Append', 'Input', 'Output'], 'As', file_fileno
def close_stmt():       return 'Close', file_fileno
def file_fileno():      return '#', expr

# For loop rules
def for_stmt():         return 'For', var, '=', for_range_decl
def for_range_decl():   return [ ( expr, 'To', expr, 'Step', expr ), ( expr, 'To', expr ) ]
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
def input_file():       return ( '#', expr, ',', input_vars )
def input_vars():       return var, ZeroOrMore( ',', var )


# Print rules
def print_stmt():       return [ '?', 'Print' ], [ print_fileno, '' ], Optional( print_params )
def print_params():     return [ [ print_using_fmt, print_exprs ],
                                 ( print_exprs, print_using_fmt ) ]
def print_fileno():     return '#', expr, ','
def print_using_fmt():  return 'Using', [ string, var], ';', print_exprs
def print_exprs():      return print_expr, ZeroOrMore( print_sep, print_expr )
def print_expr():       return Not( 'Using' ), expr # Any expr but the keyword 'Using'
def print_sep():        return [ ',', ';' ]


# branch instructions
def branch_stmts():     return [ on_sprite_stmt, on_interval_stmt, on_branch_stmt, branch_stmt, return_stmt ]
def on_sprite_stmt():   return 'On', 'Sprite', 'Gosub', address
def on_interval_stmt(): return 'On', ( 'Interval', '=', expr ), 'Gosub', comma_sep_addrs
def on_branch_stmt():   return 'On', expr, branch_tk, comma_sep_addrs
def branch_stmt():      return branch_tk, address
def return_stmt():      return 'Return', Optional( address )
def comma_sep_addrs():  return Optional( address ), ZeroOrMore( comma, Optional( address ) )
def address():          return [ label_clause, numeral ]
def branch_tk():        return [ goto_tk, gosub_tk ]
def goto_tk():          return [ 'Goto' ]
def gosub_tk():         return [ 'Gosub' ]


# label stmt
def label_stmt():       return label_addr, Optional( label_stmt )
def label_addr():       return '@', RegEx(r'[_A-Z][_A-Z0-9]*'), Optional(':') # some BASIC dialects require the ending ':'
def label_clause():     return RegEx(r'[_A-Z][_A-Z0-9]*')


# branch related statements
def switcher_stmt():    return switchers_tk, switch_tk
def switchers_tk():     return [ interval_tk, sprite_tk ]
def switch_tk():        return [ 'On', 'Off', 'Stop' ]
def interval_tk():      return [ 'Interval' ]
def sprite_tk():        return [ 'Sprite' ]


# Exit rules
def exit_stmt():        return 'Exit', [ 'Function', 'Sub' ]

# Graphics statements
def graphics_stmts():   return [ draw_stmt, circle_stmt, colordef_stmt, color_stmt, copy_stmt, line_stmt, paint_stmt, preset_stmt,
                                 pset_stmt, put_kanji_stmt, put_sprite_stmt, screen_stmt, set_page_stmt ]
def draw_stmt():        return 'Draw', expr
def circle_stmt():      return 'Circle', g_ostep_point, circle_stmt_args
def circle_stmt_args(): return Optional( comma, g_color, Optional( comma, g_color ) )
def colordef_stmt():    return 'Color', '=', [ 'New', 'Restore', ( '(', expr, comma, expr, comma, expr, comma, expr, ')' ) ]
def color_stmt():       return 'Color', Optional( g_color ), Optional( comma, g_color, Optional( comma, g_color ) )
def copy_stmt():        return 'Copy', g_copy_src, 'To', g_copy_dst
def line_stmt():        return 'Line', Optional( g_ostep_point ), g_dst_ostep_point, line_stmt_args
def line_stmt_args():   return Optional( comma, g_color, Optional( comma, g_shape, Optional( comma, g_optor ) ) )
def paint_stmt():       return 'Paint', g_ostep_point, paint_stmt_args
def paint_stmt_args():  return Optional( comma, g_color, Optional( comma, g_color ) )
def preset_stmt():      return 'Preset', g_ostep_point, preset_stmt_args
def preset_stmt_args(): return Optional( comma, g_color, Optional( comma, g_optor ) )
def pset_stmt():        return 'Pset', g_ostep_point, pset_stmt_args
def put_kanji_stmt():   return 'Put', 'Kanji', g_ostep_point, g_jis_code, g_color, g_optor, g_mode
def pset_stmt_args():   return Optional( comma, g_color, Optional( comma, g_optor ) )
def put_sprite_stmt():  return 'Put', 'Sprite', expr, comma, g_ostep_point, put_sprite_stmt_args
def put_sprite_stmt_args(): return Optional( comma, g_color, Optional( comma, g_pttn_num ) )
def screen_stmt():      return 'Screen', Optional( g_mode ), Optional( comma ), Optional( g_sprite_size ), Optional( comma ), Optional( g_key_click ), Optional( comma ), Optional( g_baud_rate ), Optional( comma ), Optional( g_printer_type ), Optional( comma ), Optional( g_interlace_mode )
def set_page_stmt():    return 'Set', 'Page', g_page, Optional( comma, g_page )

def g_jis_code():       return expr
def g_radius():         return expr
def g_color():          return expr
def g_tracing_start():  return expr
def g_tracing_end():    return expr
def g_aspect():         return expr
def g_shape():          return [ 'BF', 'B' ]
def g_optor():          return [ 'And', 'Or', 'Preset', 'Pset', 'Xor', 'Tand', 'Tor', 'Tpreset', 'Tpset', 'Txor' ]
def g_page():           return expr
def g_mode():           return expr
def g_sprite_size():    return expr
def g_key_click():      return expr
def g_baud_rate():      return expr
def g_printer_type():   return expr
def g_interlace_mode(): return expr
def g_direction():      return expr
def g_pttn_num():       return expr
def g_dst_ostep_point():return RegEx('-'), Optional( RegEx( 'Step' ) ), g_point
def g_ostep_point():    return Optional( RegEx( 'Step' ) ), g_point
def g_point():          return '(', expr, comma, expr, ')'
def g_copy_src():       return [ ( g_point, g_dst_ostep_point, Optional( comma, g_page ) ),
                                 ( g_array, Optional( comma, g_direction ) ),
                                 ( filepath, Optional( comma, g_direction ) ) ]
def g_copy_dst():       return [ ( g_point, Optional( comma, g_page, Optional( comma, g_optor ) ) ),
                                 ( filepath ),
                                 ( g_array ) ]
def g_array():          return alphanum_name, Optional( type_des )

# Play instruction
def play_stmt():        return 'Play', Optional( '#', expr, ',' ), Optional( expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr, Optional( ',', expr ) ) ) ) ) ) ) ) ) ) ) ) )


# Resume instruction
def resume_stmt():      return 'Resume', [ next_tk, numeral ]
def next_tk():          return 'Next'


# Instruction that accepts comma-separated lists.
def comma_lst_stmt():   return comma_lst_st_tk
def comma_lst_st_tk():  return [ 'Erase' ]


# Instruction with no parameters
def paramless_stmt():   return [ 'Beep', 'Cls', 'End', 'Nop' ]


# Single param instruction
def simple_stmt():      return simple_stmt_tk, expr
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
def expr():             return eqv_op, ZeroOrMore( RegEx(r'Imp'), eqv_op )
def eqv_op():           return xor_op, ZeroOrMore( RegEx(r'Eqv'), xor_op )
def xor_op():           return or_op, ZeroOrMore( RegEx(r'Xor'), or_op )
def or_op():            return and_op, ZeroOrMore( RegEx(r'or'), and_op )
def and_op():           return not_op, ZeroOrMore( RegEx(r'And'), not_op )
def not_op():           return ZeroOrMore( RegEx(r'Not') ), comp_op
def comp_op():          return add_op, ZeroOrMore( comptor, add_op )
def case_comp_op():     return comptor, add_op
def add_op():           return mod_op, ZeroOrMore( add_or_sub_tk, mod_op )
def mod_op():           return idiv_op, ZeroOrMore( RegEx(r'Mod'), idiv_op )
def idiv_op():          return mul_op, ZeroOrMore( RegEx(r'\\'), mul_op )
def mul_op():           return neg_op, ZeroOrMore( mul_or_div_tk, neg_op )
def neg_op():           return ZeroOrMore( signal ), exp_op
def exp_op():           return optor, ZeroOrMore( RegEx('\^'), optor )
def optor():            return [ ( '(', expr, ')' ), numeral, string, rvalue ]


# General
def exprs():            return expr, ZeroOrMore( ',', expr )

def rvalue():           return [ array, scalar ]
def var():              return [ array, scalar ]
def array():            return array_name, array_args
def array_name():       return alphanum_name, Optional( type_des )
def array_args():       return '(', Optional( exprs ), ')'
def scalar():           return scalar_name
def scalar_name():      return alphanum_name, Optional( type_des )

def comptor():          return [ '=', '<>', '<=', '<', '>=', '>']
def non_quote_char():   return RegEx(r'[^"]')
def any_char():         return RegEx(r'[^\n]')
def numeral():          return [ fractional, integer ]
def fractional():       return Optional( add_or_sub_tk ), Optional( digit ), '.', ZeroOrMore( digit )
def integer():          return [ ( signal, OneOrMore( digit ) ),
                                 ( signal, hex_prefix, OneOrMore( hex_digit ) ),
                                 ( signal, oct_prefix, OneOrMore( oct_digit ) ),
                                 ( signal, bin_prefix, OneOrMore( bin_digit ) ) ]
def digit():            return RegEx(r'[0-9]')
def hex_prefix():       return RegEx(r'\&H')
def hex_digit():        return RegEx(r'[0-9A-F]')
def oct_prefix():       return RegEx(r'\&O')
def oct_digit():        return RegEx(r'[0-7]')
def bin_prefix():       return RegEx(r'\&B')
def bin_digit():        return RegEx(r'[01]')
def filepath():         return string, ''
def string():           return '"', Sequence( ZeroOrMore( non_quote_char ), skipws=False ), '"'
def opt_stmt_sep():     return Optional( statement_sep )
def statement_sep():    return [ ( new_lines, ':', new_lines ), OneOrMore( new_line ) ]
def signal():           return Optional( add_or_sub_tk )
def reserved():         return [ 'And', 'As', 'Imp', 'Eqv', 'Mod', 'Xor', 'Or' ] # 'To' and others?
# Mimics MSX-BASIC parsing rules by parsing "aimpb" as "A IMP B"
#def alphanum_name():    return Not( reserved ), RegEx(r'[A-Z]'), ZeroOrMore( Not( reserved ), RegEx(r'[A-Z0-9]') )
def alphanum_name():    return RegEx(r'[A-Z][_A-Z0-9]*')
def type_des():         return RegEx(r'[$#!%]')
def comma():            return RegEx(',')
def new_lines():        return ZeroOrMore("\n")
def new_line():         return "\n"


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
    return ParserPython(program, comment_def=comments, reduce_tree=False, ignore_case=True, ws='\t ', skipws=True, debug=debug_mode)
