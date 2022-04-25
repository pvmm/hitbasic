import random

from contextlib import suppress

from hitbasic.msx import types, builtins 

from hitbasic.helpers import *


class SymbolTable(dict):

    def __init__(self):
        # string, integer, double, single
        self['_global'] = {
                # Use type suffix so different variable types don't collide.
                '_basic_vars': { types.String: {}, types.Integer: {}, types.Double: {}, types.Single: {} },
                '_hitbasic_vars': {},
                '_functions': {},
                '_builtins': builtins(),
                '_labels': {},
                '_prefix_counters': {}
        }


    def check_label(self, identifier, context='_global'):
        return self[context]['_labels'].get(identifier)


    def get_label(self, identifier, context='_global'):
        return self[context]['_labels'][identifier]


    def update_label(self, identifier, line_number, context='_global'):
        if self[context]['_labels'].get(identifier):
            self[context]['_labels'][identifier] = line_number
        else:
            raise NameNotDeclared(identifier)


    def register_label(self, prefix=None, context='_global'):
        'register label name and return it'
        if self[context]['_prefix_counters'].get(prefix) is None:
            self[context]['_prefix_counters'][prefix] = 0
            return prefix + str(self[context]['_prefix_counters'][prefix])
        else:
            self[context]['_prefix_counters'][prefix] += 1
            return prefix + str(self[context]['_prefix_counters'][prefix])


    def store_label(self, label, context='_global'):
        assert(label.keyword != None)
        if self[context]['_labels'].get(label.keyword):
            raise NameRedefined(label.keyword)
        self[context]['_labels'][label.keyword] = label.line_num


    def check_builtin(self, identifier, context='_global'):
        return self[context]['_builtins'].get(identifier.title())


    def register_function(self, identifier, params=(), type=None, context='_global'):
        if self[context]['_functions'].get(identifier):
            raise NameRedefined(identifier)
        if type == None: print("* warning: function '%s' return type is undefined." % identifier)
        self[context]['_functions'][identifier] = types.Function(identifier, params, type)
        self.store_label(identifier) # every function has a label with the same name


    def check_function(self, identifier, params=None, no_exception=True, context='_global'):
        try:
            function = self[context]['_functions'][identifier]
            if params != None: function.check_params(params)
            return function
        except KeyError:
            if no_exception: return None
            printable_id = types.strip_attrs_from_id(identifier)
            raise NameNotDeclared(printable_id)


    def check_hitbasic_var(self, identifier, params=None, no_exception=True, context='_global'):
        assert type(identifier) == str
        try:
            var = self[context]['_hitbasic_vars'][identifier]
            if params != None: var.check_boundaries(params)
            return var
        except KeyError:
            if no_exception: return None
            printable_id = types.strip_attrs_from_id(identifier)
            raise NameNotDeclared(printable_id)


    def get_hitbasic_var(self, identifier, params=None, context='_global'):
        'like check_hitbasic_var, but meaner'
        assert type(identifier) == str
        try:
            var = self[context]['_hitbasic_vars'][identifier]
            if params != None: var.check_boundaries(params)
            return var
        except KeyError:
            printable_id = types.strip_attrs_from_id(identifier)
            raise NameNotDeclared(printable_id)


    def check_basic_var(self, identifier, params=None, type=None, context='_global'):
        'check if basic var exists'
        assert __builtins__['type'](identifier) == str
        type = types.get_type_from_id(identifier) or type
        with suppress(KeyError):
            var = self[context]['_basic_vars'][type].get(identifier.upper())
            if params != None: var.check_boundaries(params)
            return var
        return self[context]['_basic_vars'][type].get(identifier.upper())


    def check_id(self, identifier, params=(), type=None, context='_global'):
        'find anything that matches'
        assert __builtins__['type'](identifier) == str
        if (result := self.check_builtin(identifier, context=context)):
            return result
        if (result := self.check_hitbasic_var(identifier, params=params, context=context)):
            return result
        if (result := self.check_basic_var(identifier, params=params, type=type, context=context)):
            return result
        if (result := self.check_function(identifier, params=params, context=context)):
            return result
        return None


    def base36(self, num, base=36, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
        assert type(num) == int
        return ((num == 0) and numerals[0]) or (self.base36(num // base, base,
            numerals).lstrip(numerals[0]) + numerals[num % base])


    def register_variable(self, hb_id=None, basic_id=None, ranges=(), init_value=None, type=None, node=None, context='_global'):
        'Register a HitBasic long named variable in the symbol table.'
        if hb_id == None:
            value = random.randint(10, 960)
            if value > 35 and value < 360: value += 360
            hb_id = self.base36(value)
            if type == None:
                type = types.DEFAULT_TYPE
        elif hb_id[-1] in types.TYPE_CHARS:
            # detect type descriptor in hitbasic var if it exists.
            if type != None and types.get_type_from_id(hb_id) != type:
                raise TypeMismatch(types.printable(type), types.printable(types.get_type_from_id(hb_id)))
            type = types.get_type_from_id(hb_id)
        elif type == None:
            type = types.current_default_type
        type_char = types.get_basic_typedes_char(type)

        # Create basic_id if it didn't exist.
        if basic_id == None:
            basic_id = self.generate_basic_var_id(hb_id)
        else:
            basic_id = types.strip_attrs_from_id(basic_id)

        vl = vr = int(basic_id, 36)
        suffix = '()' if ranges else ''
        v = (basic_id + type_char + suffix).upper()
        hb_id = hb_id + suffix if hb_id else None

        if hb_id and self.check_hitbasic_var(hb_id, params=None, context=context) == None \
                and self.check_basic_var(v, params=None, type=type, context=context) == None:
            var = types.BASICVar(v, reference=hb_id, ranges=ranges, type=type, init_value=init_value)
            if hb_id: self[context]['_hitbasic_vars'][hb_id] = var
            self[context]['_basic_vars'][type][v] = var
            return var

        # Slow and stupid method of getting next available MSX BASIC var name.
        single_length = range(10, 35)
        double_length = range(360, 1295)

        while True:
            vl -= 1; vr += 1
            if vr > 1295:
                vr = 10
            elif vr > 35 and vr < 360:
                vr = 360
            if vl < 10: vl = 1295
            elif vl > 35 and vl < 360: vl = 35
            #debug(f'{vr=}, {vl=}')

            if vr in double_length:
                v = (self.base36(vr) + type_char + suffix).upper()
                if hb_id and self.check_hitbasic_var(hb_id, params=None, context=context) == None \
                        and self.check_basic_var(v, params=None, type=type, context=context) == None:
                    var = types.BASICVar(v, reference=hb_id, ranges=ranges, type=type, init_value=init_value)
                    if hb_id: self[context]['_hitbasic_vars'][hb_id] = var
                    self[context]['_basic_vars'][type][v] = var
                    return var
            elif vr in single_length:
                v = (self.base36(vr) + type_char + suffix).upper()
                if hb_id and self.check_hitbasic_var(hb_id, params=None, context=context) == None \
                        and self.check_basic_var(v, type=type, params=None, context=context) == None:
                    var = types.BASICVar(v, reference=hb_id, ranges=ranges, type=type, init_value=init_value)
                    if hb_id: self[context]['_hitbasic_vars'][hb_id] = var
                    self[context]['_basic_vars'][type][v] = var
                    return var
            elif vl in double_length:
                v = (self.base36(vl) + type_char + suffix).upper()
                if hb_id and self.check_hitbasic_var(hb_id, params=None, context=context) == None \
                        and self.check_basic_var(v, type=type, params=None, context=context) == None:
                    var = types.BASICVar(v, reference=hb_id, ranges=ranges, type=type, init_value=init_value)
                    if hb_id: self[context]['_hitbasic_vars'][hb_id] = var
                    self[context]['_basic_vars'][type][v] = var
                    return var
            elif vl in single_length:
                v = (self.base36(vl) + type_char + suffix).upper()
                if hb_id and self.check_hitbasic_var(hb_id, params=None, context=context) == None \
                        and self.check_basic_var(v, type=type, params=None, context=context) == None:
                    var = types.BASICVar(v, reference=hb_id, ranges=ranges, type=type, init_value=init_value)
                    if hb_id: self[context]['_hitbasic_vars'][hb_id] = var
                    self[context]['_basic_vars'][type][v] = var
                    return var
            else:
                if len(self[context]['_basic_vars'][type]) > 950:
                    raise NamespaceExausted()


    def generate_basic_var_id(self, name):
        'generate short two letter variable identifier from HitBasic variable name'
        name = types.strip_attrs_from_id(name)
        name = (name[0].upper() + name[1:]).replace('_', '') # transform into Pascal case without underscores
        if len(name) > 2:
            new_name = ''.join(filter(lambda x: x.isupper(), name))[0:2]
            if len(new_name) > 0:
                return new_name
            name = name[0].upper() + name[1:]
            new_name = str().join(filter(lambda x: x.isalnum() and x == x.upper(),
                name))[0:2]
            return new_name
        else:
            return name


    def create_hitbasic_var(self, hb_id=None, ranges=(), type=None, init_value=None, node=None, context='_global'):
        if hb_id and self.check_hitbasic_var(hb_id):
            raise NameRedefined(hb_id)
        if hb_id:
            basic_id = self.generate_basic_var_id(hb_id)
            var = self.register_variable(hb_id, basic_id, ranges=ranges, type=type, init_value=init_value, node=node)
        else:
            var = self.register_variable(ranges=ranges, type=type, init_value=init_value, node=node)
        return var


    def get_hitbasic_vars(self, context='_global'):
        return list(self[context]['_hitbasic_vars'].keys())


class NamespaceExhausted(Exception):
    "no valid names left to create variables"

