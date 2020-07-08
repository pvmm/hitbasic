import re

from types import SimpleNamespace

from .factory import SurrogateFactory
from .decorator import store_node

from ..symbol_table import SymbolTable
from ..helper import *
from ..exceptions import *

from .. import msx
from .. import language_types as types
from .. import language_statements as statements


class StatementVisitor:

    def check_statement_params(self, stmt, params):
        'check if statement expected parameters match user input'
        conv_types = {'i': 'Integer', 's': 'String'}
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
            code_block.append(self.create_attribution(tmp_var, param))
        target = self.symbol_table.check_label(ref.value.identifier)
        assert target is not None
        target_label = self.create_label(target)
        code_block.append(self.create_statement('Branch', target=target_label, branch_type=statements.GOSUB))
        # getting out
        return_var = self.symbol_table.get_hitbasic_var(ref.value.short())
        assert return_var is not None
        code_block.append(self.create_attribution(var, self.create_reference(return_var)))
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
                return self.create_attribution(var, expr)
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
        dml_str = make_tuple(children)
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


    def visit_exit_stmt(self, node, children):
        return self.create_statement('Return')


    def visit_input_stmt(self, node, children):
        [(arg0, [*var_list])] = children
        if type(arg0) == types.String:
            rem = self.create_sep_list(*var_list[1:])
            return self.create_statement('Input', params=(arg0, ';', var_list[0], rem), arg_sep=())
        else:
            return self.create_statement('Input', params=('#%d' % arg0.value, *var_list))


    def visit_input_prompt(self, node, children):
        prompt, vars = children
        return prompt, vars


    def visit_input_file(self, node, children):
        fileno, vars = children
        return fileno, vars


    def visit_input_vars(self, node, children):
        return children


    def visit_let_stmt(self, node, children):
        [result] = children
        return result


    def visit_line_stmt(self, node, children):
        if len(children) > 1 and isinstance(children[1], self.clause_type['point']):
            # Line [Step](x1,y1)-[Step](x2,y2) syntax
            try:
                src, dst, args = children
            except ValueError:
                src, dst, *args = children
            return self.create_statement('Line', params=(self.create_box((src.x, src.y, src.step),
                (dst.x, dst.y, dst.step)), *args))
        else:
            # Line -[Step](x,y) syntax
            try:
                dst, args = children
            except ValueError:
                dst, *args = children
            return self.create_statement('Line', params=(self.create_box((dst.x, dst.y, dst.step)), *args))


    def visit_line_stmt_args(self, node, children):
        assert children[0] == ','
        result = parse_arg_list(children[1:], nil_element=self.create_nil(), max=2)
        return result


    def visit_paint_stmt(self, node, children):
        try:
            src, args = children
        except ValueError:
            src, *args = children
        return self.create_statement('Paint', params=self.create_sep_list(src, *args))


    def visit_paint_stmt_args(self, node, children):
        assert children[0] == ','
        result = parse_arg_list(children[1:], nil_element=self.create_nil(), max=2)
        return result


    def visit_paramless_stmt(self, node, children):
        return self.create_statement(*node.flat_str().split())


    def visit_play_stmt(self, node, children):
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
        return x, y


    def visit_var_defn(self, node, children):
        var, expr = children
        return self.create_attribution(var, expr)
