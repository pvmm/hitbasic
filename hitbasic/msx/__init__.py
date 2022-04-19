from hitbasic.language_support import Function, Array, Scalar


class types:
    Integer = 0
    String = 1
    Single = 2
    Double = 3
    Any = 4
    OptInteger = 5


class attr:
    DEFAULT = 0
    READ_ONLY = 1
    WRITE_ONLY = 2


class ver:
    MSX1_BASIC = 0
    MSX2_BASIC = 1
    DISK_BASIC = 2


def builtins():
    builtins = {
            # HitBasic name: MSXBASIC name, [params=<function parameters>], [type=<return type>], [attrs=...]
            'Abs': Function('ABS', params=types.Double, type=types.Double),
            'Atn': Function('ATN', params=types.Double, type=types.Double),
            'Asc': Function('ASC$', params=types.String, type=types.Integer),
            # Not the Base instruction.
            'Base': Function('BASE', params=types.Integer, type=types.Integer),
            'Bin': Function('BIN$', params=types.Integer, type=types.Integer),
            'Cdbl': Function('CDBL', params=types.Integer, type=types.Double),
            'Chr': Function('CHR', params=types.Integer, type=types.String),
            'Cint': Function('CINT', params=types.Single, type=types.Integer),
            'Cos': Function('COS', params=types.Double, type=types.Double),
            'Csng': Function('CSNG', params=types.Single, type=types.Single),
            'Csrlin': Scalar('CSRLIN', type=types.Integer, attrs=attr.READ_ONLY),
            'Cvd': Function('CVD', params=types.String, type=types.Double),
            'Cvi': Function('CVD', params=types.String, type=types.Integer, ver=ver.DISK_BASIC),
            'Cvs': Function('CVS', params=types.String, type=types.Single, ver=ver.DISK_BASIC),
            'Dskf': Function('DSKF', params=types.Integer, type=types.Integer, ver=ver.DISK_BASIC),
            'Eof': Function('EOF', params=types.Integer, type=types.Integer),
            'Erl': Scalar('ERL', type=types.Integer, attrs=attr.READ_ONLY),
            'Err': Scalar('ERR', type=types.Integer, attrs=attr.READ_ONLY),
            'Fix': Function('FIX', params=types.Double, type=types.Integer),
            'Fre': Function('FRE', params=types.Any, type=types.Integer),
            'Hex': Function('HEX$', params=types.Integer, type=types.String),
            'Instr': Function('INSTR', params=(types.OptInteger, types.String, types.String), type=types.Integer),
            'Inkey': Scalar('INKEY$', type=types.String, attrs=attr.READ_ONLY),
            'Inp': Function('INP', params=types.Integer, type=types.Integer),
            'Int': Function('INT', params=types.Integer, type=types.Integer),
            'Left': Function('LEFT', params=(types.String, types.Integer), type=types.String),
            'Len': Function('LEN', params=(types.String), type=types.String),
            'Loc': Function('LOC', params=types.Integer, type=types.Integer, ver=ver.DISK_BASIC),
            'Lof': Function('LOF', params=types.Integer, type=types.Integer, ver=ver.DISK_BASIC),
            'Mkd': Function('MKD$', params=types.Double, type=types.String, ver=ver.DISK_BASIC),
            'Mki': Function('MKI$', params=types.Integer, type=types.String, ver=ver.DISK_BASIC),
            'Mks': Function('MKS$', params=types.Single, type=types.String, ver=ver.DISK_BASIC),
            'Mid': Array('MID$', params=(types.String, types.Integer, types.OptInteger), type=types.String),
            'Oct': Function('OCT$', params=types.Integer, type=types.String),
            'Peek': Function('PEEK', params=types.Integer, type=types.Integer),
            'Pos': Function('POS', params=types.Integer, type=types.Integer),
            'Right': Function('RIGHT$', params=(types.String, types.Integer), type=types.String),
            'Rnd': Function('RND', params=types.Integer, type=types.Double),
            'Sgn': Function('SGN', params=types.Integer, type=types.Integer),
            'Sin': Function('SIN', params=types.Double, type=types.Double),
            'Spaces': Function('SPACE$', params=(types.Integer, types.Any), type=types.String),
            'Spc': Function('SPC', params=types.Integer, type=types.String),
            'Sprite': Function('SPRITE$', params=types.Integer, type=types.String),
            'Sqr': Function('SQR', params=types.Double, type=types.Double),
            'Stick': Function('STICK', params=types.Integer, type=types.Integer),
            'Str': Function('STR', params=types.Integer, type=types.String),
            'Strig': Function('STRIG', params=types.Integer, type=types.Integer),
            'String': Function('STRING$', params=(types.Integer, types.Any), type=types.String),
            'Tab': Function('TAB', params=types.Integer, type=types.String),
            'Tan': Function('TAN', params=types.Double, type=types.Double),
            'Time': Scalar('TIME', type=types.Integer),
            'Usr': Function('USR', params=types.Integer, type=types.Integer),
            'Usr0': Function('USR0', params=types.Integer, type=types.Integer),
            'Usr1': Function('USR1', params=types.Integer, type=types.Integer),
            'Usr2': Function('USR2', params=types.Integer, type=types.Integer),
            'Usr3': Function('USR3', params=types.Integer, type=types.Integer),
            'Usr4': Function('USR4', params=types.Integer, type=types.Integer),
            'Usr5': Function('USR5', params=types.Integer, type=types.Integer),
            'Usr6': Function('USR6', params=types.Integer, type=types.Integer),
            'Usr7': Function('USR7', params=types.Integer, type=types.Integer),
            'Usr8': Function('USR8', params=types.Integer, type=types.Integer),
            'Usr9': Function('USR9', params=types.Integer, type=types.Integer),
            'Val': Function('VAL', params=types.String, type=types.Integer),
            'Vdp': Array('VDP', params=types.Integer, type=types.Integer),
            'Vpeek': Function('VPEEK', params=types.Integer, type=types.Integer),
            'Maxfiles': Scalar('MAXFILES', type=types.Integer, attrs=attr.WRITE_ONLY),
    }

    # Also register String-returning functions with -$ suffix for MSX-BASIC compatibility.
    for identifier, value in list(builtins.items()):
        if '$' in builtins[identifier].identifier: # Because SPC() and TAB() ruins everything
            builtins[f'{identifier}$'] = value

    return builtins


