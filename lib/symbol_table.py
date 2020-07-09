from contextlib import suppress
from random import randint

from . import msx
from . import language_types as types
from . import version

from .helper import *


class SymbolTable(dict):

    def __init__(self):
        # string, integer, double, single
        self['_version'] = version.CURRENT_VERSION.rsplit('-')[0]
        self['_global'] = {
                # different variable types don't collide.
                '_basic_vars': { types.String: {}, types.Integer: {}, types.Double: {}, types.Single: {} },
                '_hitbasic_vars': {},
                '_functions': {},
                '_builtins': self.predefined_identifiers(),
                '_labels': {},
                '_prefix_counters': {}
        }


    def predefined_identifiers(self):
        builtins = {
                # HitBasic name: MSXBASIC name, [params=<function parameters>], [type=<return type>], [attrs=...]
                'Abs()': types.BuiltIn('ABS()', params=types.Double, type=types.Double),
                'Atn()': types.BuiltIn('ATN()', params=types.Double, type=types.Double),
                'Asc()': types.BuiltIn('ASC$()', params=types.String, type=types.Integer),
                # Not the Base instruction.
                'Base()': types.BuiltIn('BASE()', params=types.Integer, type=types.Integer),
                'Bin()': types.BuiltIn('BIN$()', params=types.Integer, type=types.Integer),
                'Cdbl()': types.BuiltIn('CDBL()', params=types.Integer, type=types.Double),
                'Chr()': types.BuiltIn('CHR()', params=types.Integer, type=types.String),
                'Cint()': types.BuiltIn('CINT()', params=types.Single, type=types.Integer),
                'Cos()': types.BuiltIn('COS()', params=types.Double, type=types.Double),
                'Csng()': types.BuiltIn('CSNG()', params=types.Single, type=types.Single),
                'Csrlin': types.BuiltIn('CSRLIN', type=types.Integer, attrs=types.READ_ONLY),
                'Cvd()': types.BuiltIn('CVD()', params=types.String, type=types.Double),
                'Cvi()': types.BuiltIn('CVD()', params=types.String, type=types.Integer, ver=msx.DISK_BASIC),
                'Cvs()': types.BuiltIn('CVS()', params=types.String, type=types.Single, ver=msx.DISK_BASIC),
                'Dskf()': types.BuiltIn('DSKF()', params=types.Integer, type=types.Integer, ver=msx.DISK_BASIC),
                'Eof()': types.BuiltIn('EOF()', params=types.Integer, type=types.Integer),
                'Erl': types.BuiltIn('ERL', type=types.Integer, attrs=types.READ_ONLY),
                'Err': types.BuiltIn('ERR', type=types.Integer, attrs=types.READ_ONLY),
                'Fix()': types.BuiltIn('FIX()', params=types.Double, type=types.Integer),
                'Fre()': types.BuiltIn('FRE()', params=types.Any, type=types.Integer),
                'Hex()': types.BuiltIn('HEX$()', params=types.Integer, type=types.String),
                'Instr()': types.BuiltIn('INSTR()', params=(types.OptInteger, types.String, types.String), type=types.Integer),
                'Inkey': types.BuiltIn('INKEY$', type=types.String, attrs=types.READ_ONLY),
                'Inp()': types.BuiltIn('INP()', params=types.Integer, type=types.Integer),
                'Int()': types.BuiltIn('INT()', params=types.Integer, type=types.Integer),
                'Left()': types.BuiltIn('LEFT()', params=(types.String, types.Integer), type=types.String),
                'Len()': types.BuiltIn('LEN()', params=(types.String), type=types.String),
                'Loc()': types.BuiltIn('LOC()', params=types.Integer, type=types.Integer, ver=msx.DISK_BASIC),
                'Lof()': types.BuiltIn('LOF()', params=types.Integer, type=types.Integer, ver=msx.DISK_BASIC),
                # Not to be confused with the MID$ instruction.
                'Mkd()': types.BuiltIn('MKD$()', params=types.Double, type=types.String, ver=msx.DISK_BASIC),
                'Mki()': types.BuiltIn('MKI$()', params=types.Integer, type=types.String, ver=msx.DISK_BASIC),
                'Mks()': types.BuiltIn('MKS$()', params=types.Single, type=types.String, ver=msx.DISK_BASIC),
                'Mid()': types.BuiltIn('MID$()', params=(types.String, types.String, types.OptInteger), type=types.String),
                'Oct()': types.BuiltIn('OCT$()', params=types.Integer, type=types.String),
                'Peek()': types.BuiltIn('PEEK()', params=types.Integer, type=types.Integer),
                'Pos()': types.BuiltIn('POS()', params=types.Integer, type=types.Integer),
                'Right()': types.BuiltIn('RIGHT$()', params=(types.String, types.Integer), type=types.String),
                'Rnd()': types.BuiltIn('RND()', params=types.Integer, type=types.Double),
                'Sgn()': types.BuiltIn('SGN()', params=types.Integer, type=types.Integer),
                'Sin()': types.BuiltIn('SIN()', params=types.Double, type=types.Double),
                'Spaces()': types.BuiltIn('SPACE$()', params=(types.Integer, types.Any), type=types.String),
                'Spc()': types.BuiltIn('SPC()', params=types.Integer, type=types.String),
                'Sprite()': types.BuiltIn('SPRITE$()', params=types.Integer, type=types.String),
                'Sqr()': types.BuiltIn('SQR()', params=types.Double, type=types.Double),
                'Stick()': types.BuiltIn('STICK()', params=types.Integer, type=types.Integer),
                'Str()': types.BuiltIn('STR()', params=types.Integer, type=types.String),
                'Strig()': types.BuiltIn('STRIG()', params=types.Integer, type=types.Integer),
                'String()': types.BuiltIn('STRING$()', params=(types.Integer, types.Any), type=types.String),
                'Tab()': types.BuiltIn('TAB()', params=types.Integer, type=types.String),
                'Tan()': types.BuiltIn('TAN()', params=types.Double, type=types.Double),
                'Time': types.BuiltIn('TIME', type=types.Integer),
                'Usr()': types.BuiltIn('USR()', params=types.Integer, type=types.Integer),
                'Usr0()': types.BuiltIn('USR0()', params=types.Integer, type=types.Integer),
                'Usr1()': types.BuiltIn('USR1()', params=types.Integer, type=types.Integer),
                'Usr2()': types.BuiltIn('USR2()', params=types.Integer, type=types.Integer),
                'Usr3()': types.BuiltIn('USR3()', params=types.Integer, type=types.Integer),
                'Usr4()': types.BuiltIn('USR4()', params=types.Integer, type=types.Integer),
                'Usr5()': types.BuiltIn('USR5()', params=types.Integer, type=types.Integer),
                'Usr6()': types.BuiltIn('USR6()', params=types.Integer, type=types.Integer),
                'Usr7()': types.BuiltIn('USR7()', params=types.Integer, type=types.Integer),
                'Usr8()': types.BuiltIn('USR8()', params=types.Integer, type=types.Integer),
                'Usr9()': types.BuiltIn('USR9()', params=types.Integer, type=types.Integer),
                'Val()': types.BuiltIn('VAL()', params=types.String, type=types.Integer),
                # Not to be confused with the Vdp instruction.
                'Vdp()': types.BuiltIn('VDP()', params=types.Integer, type=types.Integer),
                'Vpeek()': types.BuiltIn('VPEEK()', params=types.Integer, type=types.Integer),
                'Maxfiles': types.BuiltIn('MAXFILES', type=types.Integer, attrs=types.WRITE_ONLY),
        }
        # Also register String-returning functions with -$ suffix for MSX-BASIC compatibility.
        for identifier, value in list(builtins.items()):
            if '$' in builtins[identifier].identifier: # Because SPC() and TAB() ruins everything
                tag = types.strip_attrs_from_id(identifier)
                is_function = identifier.endswith('()')
                builtins[tag + '$' + ('()' if is_function else '')] = value
        return builtins


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
        identifier = label.identifier if hasattr(label, 'identifier') else label
        try:
            line_number = label.line_number or identifier
        except AttributeError:
            line_number = identifier
        if self[context]['_labels'].get(identifier):
            raise NameRedefined(identifier)
        self[context]['_labels'][identifier] = line_number


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
            var = self[context]['_basic_vars'][type.__name__].get(identifier.upper())
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


    def register_variable(self, hbid=None, basic_id=None, ranges=(), init_value=None, type=None, node=None, context='_global'):
        if hbid == None:
            value = randint(10, 960)
            if value > 35 and value < 360: value += 360
            hbid = self.base36(value)
            if type == None:
                type = types.DEFAULT_TYPE
        elif hbid[-1] in types.TYPE_CHARS:
            # detect type descriptor in hitbasic var if it exists.
            if type != None and types.get_type_from_id(hbid) != type:
                raise TypeMismatch(types.printable(type), types.printable(types.get_type_from_id(hbid)))
            type = types.get_type_from_id(hbid)
        elif type == None:
            type = types.current_default_type
        type_char = types.get_basic_type_char(type)

        # Create basic_id if it didn't exist.
        if basic_id == None:
            basic_id = self.generate_basic_var_id(hbid)
        else:
            basic_id = types.strip_attrs_from_id(basic_id)

        vl = vr = int(basic_id, 36)
        suffix = '()' if ranges else ''
        v = (basic_id + type_char + suffix).upper()
        hbid = hbid + suffix if hbid else None

        if hbid and self.check_hitbasic_var(hbid, params=None, context=context) == None \
                and self.check_basic_var(v, params=None, type=type, context=context) == None:
            var = types.BASICVar(v, reference=hbid, ranges=ranges, type=type, init_value=init_value)
            if hbid: self[context]['_hitbasic_vars'][hbid] = var
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
                if hbid and self.check_hitbasic_var(hbid, params=None, context=context) == None \
                        and self.check_basic_var(v, params=None, type=type, context=context) == None:
                    var = types.BASICVar(v, reference=hbid, ranges=ranges, type=type, init_value=init_value)
                    if hbid: self[context]['_hitbasic_vars'][hbid] = var
                    self[context]['_basic_vars'][type][v] = var
                    return var
            elif vr in single_length:
                v = (self.base36(vr) + type_char + suffix).upper()
                if hbid and self.check_hitbasic_var(hbid, params=None, context=context) == None \
                        and self.check_basic_var(v, type=type, params=None, context=context) == None:
                    var = types.BASICVar(v, reference=hbid, ranges=ranges, type=type, init_value=init_value)
                    if hbid: self[context]['_hitbasic_vars'][hbid] = var
                    self[context]['_basic_vars'][type][v] = var
                    return var
            elif vl in double_length:
                v = (self.base36(vl) + type_char + suffix).upper()
                if hbid and self.check_hitbasic_var(hbid, params=None, context=context) == None \
                        and self.check_basic_var(v, type=type, params=None, context=context) == None:
                    var = types.BASICVar(v, reference=hbid, ranges=ranges, type=type, init_value=init_value)
                    if hbid: self[context]['_hitbasic_vars'][hbid] = var
                    self[context]['_basic_vars'][type][v] = var
                    return var
            elif vl in single_length:
                v = (self.base36(vl) + type_char + suffix).upper()
                if hbid and self.check_hitbasic_var(hbid, params=None, context=context) == None \
                        and self.check_basic_var(v, type=type, params=None, context=context) == None:
                    var = types.BASICVar(v, reference=hbid, ranges=ranges, type=type, init_value=init_value)
                    if hbid: self[context]['_hitbasic_vars'][hbid] = var
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


    def create_hitbasic_var(self, hbid=None, ranges=(), type=None, init_value=None, node=None, context='_global'):
        if hbid:
            basic_id = self.generate_basic_var_id(hbid)
            var = self.register_variable(hbid, basic_id, ranges=ranges, type=type, init_value=init_value, node=node)
        else:
            var = self.register_variable(ranges=ranges, type=type, init_value=init_value, node=node)
        return var


    def get_hitbasic_vars(self, context='_global'):
        return list(self[context]['_hitbasic_vars'].keys())


class NamespaceExhausted(Exception):
    "no valid names left to create variables"

