import re

from types import SimpleNamespace

from .decorator import store_node

from ..factory import SurrogateFactory, factory
from ..symbol_table import SymbolTable
from ..helper import *
from ..exceptions import *

from .. import msx
from .. import language_types as types
from .. import language_clauses as clauses
from .. import language_statements as statements


class StatementVisitor:

    def check_arch(self, value):
        if self.basic_ver < value: raise WrongBASICVersion(msx.VERSION_STR[value], msx.VERSION_STR[self.arch])


    def check_statement_params(self, stmt, params):
        'check if statement expected parameters match user input'
        conv_types = {'i': 'Integer', 'o': 'Operator', 'p': 'Point', 's': 'String'}
        reg_ex = statements.create_regexp(msx.arch[self.arch].stmt_lib(stmt).pattern) # max=13 elements
        signature = statements.create_signature(params)
        if (match := re.match(reg_ex.pattern, signature)):
            if len(match.group(1)) > 0 and (epos := len(match.group(1)) - len(match.group(0))):
                raise self.create_exception(TypeMismatch, conv_types[reg_ex.type(epos)],
                                            conv_types[signature[epos]],
                                            msx.arch[self.arch].stmt_lib(stmt).names[epos])
        else:
            raise self.create_exception(MissingOperand, 'expected parameters')


    def write_vfc_subroutine(self, var, ref):
        'variable/function-call-attribution subroutine'
        code_block = []
        # going in
        for p_var, param in zip(ref.value.params, ref.params):
            tmp_var = self.create_reference(p_var, node=param)
            assert isinstance(tmp_var, factory.clause_type['reference'])
            code_block.append(self.create_statement('Let', params=self.create_attribution(tmp_var, param)))
        target = self.symbol_table.check_label(ref.value.identifier)
        assert target is not None
        target_label = self.create_label(target)
        code_block.append(self.create_statement('Branch', target=target_label, branch_type=statements.GOSUB))
        # getting out
        return_var = self.symbol_table.get_hitbasic_var(ref.value.short())
        assert return_var is not None
        assert isinstance(var, factory.clause_type['reference'])
        code_block.append(self.create_statement('Let', params=self.create_attribution(var, self.create_reference(return_var))))
        return self.create_statement('Multiple', code_block=code_block)


    def visit_statements(self, node, children):
        return flatten(children)


    def visit_statement(self, node, children):
        if len(children):
            return children.pop()
        return children


    def visit_attr_stmt(self, node, children):
        var, expr = children
        if types.compatible_types(var.type, expr.type):
            if type(expr.value) != types.Function:
                assert isinstance(var, factory.clause_type['reference'])
                return self.create_statement('Let', params=self.create_attribution(var, expr))
            else:
                # extra glue code necessary if rvalue is a function
                return self.write_vfc_subroutine(var=var, ref=expr) # caller node
        else:
            raise self.create_exception(TypeMismatch, types.printable_type(expr), types.printable_type(var),
                                        var.value.reference, pos=node[0].position)


    def visit_branch_stmt(self, node, children):
        stmt, label = children
        return self.create_statement(stmt, params='@%s' % label)


    def visit_draw_stmt(self, node, children):
        dml_str = children
        return self.create_statement('Draw', params=dml_str)


    def visit_circle_stmt(self, node, children):
        try:
            src, args = children
        except ValueError:
            src, *args = children
        return self.create_statement('Circle', params=self.create_sep_list(src, *args))


    def visit_circle_stmt_args(self, node, children):
        # CIRCLE STEP(<X>,<Y>),<Radius>,<Color>,<TracingStart>,<TracingEnd>,<Aspect>
        assert children[0] == ','
        result = parse_arg_list(children[1:], nil_element=self.create_nil(), max=5)
        return result


    def visit_color_stmt(self, node, children):
        try:
            params = parse_arg_list(children, nil_element=self.create_nil(), max=3)
        except MissingOperand as e:
            param = node[-1]
            raise self.put_location(e, param.position)
        return self.create_statement('Color', params=params)


    def visit_colordef_stmt(self, node, children):
        # COLOR = (<Color>,<RedLuminance>,<GreenLuminance>,<BlueLuminance>)
        params = parse_comma_list(children, max=4)
        colordef = self.create_tuple(*params, use_parentheses=True)
        return self.create_statement('', params=self.create_attribution('Color', colordef))


    def visit_exit_stmt(self, node, children):
        return self.create_statement('Return')


    def visit_input_stmt(self, node, children):
        # INPUT "<Prompt>"; <Variable>,<Variable>...
        [(arg0, [*var_list])] = children
        if type(arg0) == types.String:
            if not var_list: raise MissingOperand('missing parameters after %s' % arg0.value)
            param0 = self.create_sep_list(arg0, var_list[0], sep=';')
            return self.create_statement('Input', params=(param0, *var_list[1:]))
        elif isinstance(arg0, clauses.reference):
            return self.create_statement('Input', params=(arg0, *var_list))
        elif isinstance(arg0, types.Integer):
            return self.create_statement('Input', params=('#%d' % arg0.value, *var_list))
        else:
            raise TypeMismatch('Channel', arg0.type)


    def visit_input_prompt(self, node, children):
        prompt, vars = children
        return prompt, vars


    def visit_input_file(self, node, children):
        fileno, vars = children
        return fileno, vars


    def visit_input_vars(self, node, children):
        return children


    def visit_let_stmt(self, node, children):
        # LET <Variable> = <Value>
        [result] = children
        return result


    def visit_line_stmt(self, node, children):
        # LINE STEP(<X1>,<Y1>)-STEP(<X2>,<Y2>),<Color>,<Shape>,<Operator>
        if len(children) > 1 and isinstance(children[1], clauses.TYPES['point']):
            # Line [Step](x1,y1)-[Step](x2,y2) syntax
            try:
                src, dst, args = children
            except ValueError:
                src, dst, *args = children
            self.check_statement_params('LINE', (src, dst) + make_tuple(args))
            return self.create_statement('Line', params=(self.create_box((src.x, src.y, src.step),
                (dst.x, dst.y, dst.step)), *args))
        else:
            # Line -[Step](x,y) syntax
            try:
                dst, args = children
            except ValueError:
                dst, *args = children
            self.check_statement_params('LINE', (dst,) + make_tuple(args))
            return self.create_statement('Line', params=(self.create_box((dst.x, dst.y, dst.step)), *args))


    def visit_line_stmt_args(self, node, children):
        assert children[0] == ','
        result = parse_arg_list(children[1:], nil_element=self.create_nil(), max=2)
        return result


    def visit_open_stmt(self, node, children):
        filepath, direction, fileno = children
        return self.create_statement('Open', params=(filepath, 'For', direction, 'As', '#%d' % fileno.value), sep=' ')


    def visit_open_stmt_rnd(self, node, children):
        filepath, fileno, *len = children
        return self.create_statement('Open', params=(filepath, 'As', '#%d' % fileno.value, ('Len=%d' % len[0].value) if len else None), sep=' ')


    def visit_on_branch_stmt(self, node, children):
        # ON <ConditionExpression> [GOTO|GOSUB] <LineNumber>,<LineNumber>,...
        expr, branch_type, *branch_list = children
        return self.create_statement('On', params=(expr, branch_type, self.create_sep_list(*branch_list)), sep=' ')


    def visit_on_interval_stmt(self, node, children):
        expr, dst = children
        return self.create_statement('On', params=(self.create_attribution('Interval', expr), 'Gosub', dst), sep=' ')


    def visit_on_sprite_stmt(self, node, children):
        pass


    def visit_paint_stmt(self, node, children):
        try:
            src, args = children
        except ValueError:
            src, *args = children
        self.check_statement_params('PAINT', (src,) + args)
        return self.create_statement('Paint', params=self.create_sep_list(src, *args))


    def visit_paint_stmt_args(self, node, children):
        assert children[0] == ','
        result = parse_arg_list(children[1:], nil_element=self.create_nil(), max=2)
        return result


    def visit_paramless_stmt(self, node, children):
        return self.create_statement(*node.flat_str().split())


    def visit_play_stmt(self, node, children):
        # PLAY #<Device>,"<MmlStringChannel1>","<MmlStringChannel2>",...,"<MmlStringChannel13>"
        params = children
        # detect wrong parameter count or type
        self.check_statement_params('PLAY', params)
        # Put a '#' before channel number
        if node[1].flat_str() == '#':
            if isinstance(params[0], types.Integer):
                params = '#%s' % params[0].value, *params[1:]
            else:
                raise self.create_exception(TypeMismatch, 'Channel', types.printable_type(params[0]))
        return self.create_statement('Play', params=params)


    def visit_pset_stmt(self, node, children):
        # PSET STEP(<X>,<Y>),<Color>,<Operator>
        try:
            src, args = children
        except ValueError:
            src, *args = children
        # detect wrong parameter count or type
        self.check_statement_params('PSET', params)
        return self.create_statement('Pset', params=self.create_sep_list(src, *args))


    def visit_pset_stmt_args(self, node, children):
        # PSET STEP(<X>,<Y>),<Color>,<Operator>
        assert children[0] == ','
        return parse_arg_list(children[1:], nil_element=self.create_nil(), max=2)


    def visit_preset_stmt(self, node, children):
        # PRESET STEP(<X>,<Y>),<Color>,<operator>
        try:
            src, args = children
        except ValueError:
            src, *args = children
        return self.create_statement('Preset', params=self.create_sep_list(src, *args))


    def visit_preset_stmt_args(self, node, children):
        # PRESET STEP(<X>,<Y>),<Color>,<operator>
        assert children[0] == ','
        return parse_arg_list(children[1:], nil_element=self.create_nil(), max=2)


    def visit_put_kanji_stmt(self, node, children):
        # PUT KANJI STEP(<X>,<Y>),<JIScode>,<Color>,<Operator>,<Mode>
        self.check_arch(msx.MSX_BASIC_2_0)
        raise NotImplemented()


    def visit_put_sprite_stmt(self, node, children):
        # PUT SPRITE <sprite number>,[STEP](<x>,<y>),[<color>][,<pattern number>]
        sp_num, comma, dst, args = children
        return self.create_statement('Put Sprite', params=(sp_num, dst, *args))


    def visit_put_sprite_stmt_args(self, node, children):
        # PUT SPRITE <sprite number>,[STEP](<x>,<y>),[<color>][,<pattern number>]
        assert children[0] == ','
        return parse_arg_list(children[1:], nil_element=self.create_nil(), max=2)


    def visit_screen_stmt(self, node, children):
        screen_attrs_len = len(msx.arch[self.arch].screen_attrs())
        try:
            params = parse_arg_list(children, nil_element=self.create_nil(), max=screen_attrs_len)
        except MissingOperand as e:
            param = node[-1]
            raise self.put_location(e, param.position)
        for param, attr in zip(params, msx.arch[self.arch].screen_attrs()):
            if type(param) != types.Nil and not isinstance(param, types.numeric_classes()):
                raise self.create_exception(TypeMismatch, types.printable_type(expr), types.printable_type(var),
                                            var.value.reference, pos=param.position)
            if type(param) != types.Nil and param.is_constexp and not param.literal_value() in attr:
                raise self.create_exception(IllegalFunctionCall, pos=param.position)
        return self.create_statement('Screen', params=params)


    def visit_set_page_stmt(self, node, children):
        self.check_arch(msx.MSX_BASIC_2_0)
        params = parse_arg_list(children, nil_element=self.create_nil(), max=2)
        return self.create_statement('Set Page', params=params)


    def visit_g_ostep_point(self, node, children):
        *step, (x, y) = children
        return self.create_point(x, y, bool(step))


    def visit_g_dst_ostep_point(self, node, children):
        *tokens, (x, y) = children
        tokens = tuple(token.lower() for token in tokens)
        assert tokens[0] == '-'
        step = len(tokens) > 1 and tokens[1] == 'step'
        return self.create_point(x, y, step)


    def visit_g_opt_expr(self, node, children):
        x, _, y = children
        return x, y


    def visit_g_step(self, node, children):
        return self.create_token('Step')


    def visit_g_point(self, node, children):
        x, _, y = children
        if not isinstance(x, types.Numeric):
            raise self.create_exception(TypeMismatch, 'Point', types.printable_type(x))
        if not isinstance(x, types.Numeric):
            raise self.create_exception(TypeMismatch, 'Point', types.printable_type(y))
        return x, y


    def visit_var_defn(self, node, children):
        var, expr = children
        assert isinstance(var, factory.clause_type['reference'])
        return self.create_statement('Let', params=self.create_attribution(var, expr))


    def visit_switcher_stmt(self, node, children):
        stmt, *params = children
        return self.create_statement(stmt, params=params)
