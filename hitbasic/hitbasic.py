from textx import metamodel_from_str, get_children_of_type

grammar = r"""
Program[ws=" \t"]:
    Sep*- statements*=AllStmtTypes[/(:|\n)+/] Sep*-;

MinStmtTypes[ws=" \t"]:
    DimStmt | ConditionalStmt | SelectStmt | DoLoopStmt | CloseStmt | OpenStmt | NextStmt | ForStmt |
    PrintStmt | BranchStmt | GraphicsStmt | LetStmt | DefStmt | InputStmt | PlayStmt | SwitcherStmt |
    SimpleStmt | AttrStmt; 

AllStmtTypes:
    FuncStmt | SubStmt | MinStmtTypes;

FuncStmt:           header=FuncHeads Sep*- statements*=FuncStmtTypes[/(:|\n)+/] Sep*- FuncStmtEnd;
FuncHeads:          FuncHead | FuncHeadTyped;
FuncHead:           'Function' name=Name '(' params*=FuncVarDecl[/(,|\n)+/] ')' return=FuncReturnType;
FuncHeadTyped:      'Function' name=TypedName '(' params*=FuncVarDecl[/(,|\n)+/] ')';
FuncVarDecl:        Name 'As' VarType | TypedName;
FuncStmtTypes:      !('End' 'Function')- ( FuncExitStmt | ReturnStmt | MinStmtTypes );
FuncExitStmt:       'Exit' 'Function';
ReturnStmt:         'Return' ( Var | Label );
FuncReturnType:     'As' VarType;
FuncStmtEnd:        'End' 'Function';

SubStmt:            header=SubHead Sep*- statements*=SubStmtTypes[/(:|\n)+/] Sep*- SubStmtEnd;
SubHead:            'Sub' name=Name '(' params*=SubVarDecl[/(,|\n)+/] ')';
SubVarDecl:         Name 'As' VarType | TypedName;
SubStmtTypes:       !('End' 'Sub')- ( SubExitStmt | ReturnStmt | MinStmtTypes );
SubExitStmt:        'Exit' 'Sub';
SubStmtEnd:         'End' 'Sub';

DimStmt[ws=' \t\n']:
    'Dim' vars+=DimVarDecl[/,/];

DimVarDecl:         DimVar 'As' VarType '=' DimAttr |
                    DimVar 'As' VarType |
                    DimVar '=' DimAttr |
                    DimVar;

DimVar:             name=Name ( '(' ranges*=DimRangeDecl[/,/] ')' )?;

DimRangeDecl:       NumericExp 'To' NumericExp | NumericExp;

DimAttr:            NumericExp | '{' NumericExp '}';

ConditionalStmt:    IfThenElseStmt | IfThenStmt | IfElseOneLiner | IfThenOneLiner;

IfExpressionThen:   !( 'Then' ) Expression 'Then'-;

IfElseOneLiner[ws=' \t']:
    'If' expr=IfExpressionThen statements*=OneLinerStmtTypes[/:+/ eolterm]
    'Else' statements*=OneLinerStmtTypes[/:+/ eolterm];

IfThenOneLiner[ws=' \t']:
    'If' expr=IfExpressionThen statements*=OneLinerStmtTypes[/:+/ eolterm];

OneLinerStmtTypes:  !( 'Else' )- MinStmtTypes;
//OneLinerStmtTypes:  !( EOL )- MinStmtTypes;

ThenClause: statements*=ThenStmtTypes[/:+/ eolterm];

EndIfClause: statements*=EndIfStmtTypes[/:+/ eolterm];

IfThenElseStmt:
    'If' expr=Expression ('Then' | Sep)? Sep* ThenBlock Sep* 'Else' Sep* EndIfBlock Sep* EndIfStmt;

IfThenStmt:
    'If' expr=Expression ('Then' | Sep)? Sep* EndIfBlock Sep* EndIfStmt;

ThenBlock: statements*=ThenStmtTypes[/(:|\n)+/];

EndIfStmtTypes:     !( 'End' 'If' )- MinStmtTypes;

EndIfBlock: statements*=EndIfStmtTypes[/(:|\n)+/];

ThenStmtTypes:      !( 'Else' )- MinStmtTypes;

EndIfStmt:          'End' 'If' &Sep+;

SelectStmt:
    'Select' expr=Expression Sep*- cases*=CaseStmtTypes[/(:|\n)+/] Sep*- SelectStmtEnd;

CaseStmtTypes:      !( 'End' 'Select' )- ( CaseStmt | MinStmtTypes );

CaseStmt[ws=' \t\n']:
    'Case'- ( 'Else' | expr=Expression );

SelectStmtEnd:      'End' 'Select' &Sep+;

DoLoopStmt:         'Do' condition=DoCond Sep+ statements*=DoStmtTypes[/(:|\n)+/] Sep* 'Loop' |
                    'Do' Sep+ statements*=DoStmtTypes[/(:|\n)+/] Sep* 'Loop' condition=DoCond;
DoCond:             ( 'While' | 'Until' ) expr=NumericExp;
DoStmtTypes:        !( 'Loop' )- ( ExitDoStmt | MinStmtTypes );
ExitDoStmt:         'Exit' 'Do';

CloseStmt:          'Close' Fileno;
Fileno:             '#' NumericExp;

OpenStmt:           'Open';

NextStmt:           'Next' ( vars*=Var[/,/] )?;

ForStmt:            'For' var=Var '=' range=ForRangeDecl;
ForRangeDecl:       begin=NumericExp 'to'- end=NumericExp ( 'Step'- step=NumericExp )?;

PrintStmt:          ('Print' | '?') ( fileno=PrintFileNo )? params=PrintParams;
PrintFileNo:        '#' NumericExp ',';
PrintParams:        exprs*=Expression[/(,|;)/] ( using=PrintUsing )?;
PrintUsing:         'Using' fmt=PrintUsingFmt ';' exprs+=Expression[/(,|;)/];
PrintUsingFmt:      String | Var;

BranchStmt:         'Goto' | 'Gosub';

GraphicsStmt:       'Graphics';

LetStmt:            'Let';

DefStmt:            'Def Fn';

InputStmt:          'Input' ( InputPrompt | InputFile );
InputPrompt:        ( String ';' )? vars*=Var[/,/];
InputFile:          '#' NumericExp ',' vars*=Var[/,/];

PlayStmt:           'Play';

SwitcherStmt:       'x';

SimpleStmt[ws=' \t\n']:
    keyword=KeywordStmt;

KeywordStmt:        'Beep' | 'Cls' | 'End' | 'Nop';

AttrStmt:           'Let'? definition=VarDefn;
VarDefn:            var=Var '=' expr=Expression;

VarType:
    'Boolean' | 'BOOL' | 'Integer' | 'INT' | 'String' | 'STR' | 'Single' | 'SNG' | 'Double' | 'DBL';

Label:              '@' Name;
Var:                Array | Identifier;
Array:              Identifier '(' ( subscript*=NumericExp[/,/] )? ')';
Identifier:         TypedName | Name;

String[noskipws]:
    '"' /[^"]*/ '"';

TypedName:          Name TypeDescriptor;

TypeDescriptor:     /[$#!%]/;

Name:               /[_A-Za-z][_A-Za-z0-9]*/;

Expression:         NumericExp | STRING;
NumericExp:         ImpOp; // Imp: lowest precedence operator
ImpOp:              op1=EqvOp ( 'Imp'-        op2=EqvOp )*;
EqvOp:              op1=XorOp ( 'Eqv'-        op2=XorOp )*;
XorOp:              op1=_OrOp ( 'Xor'-        op2=_OrOp )*;
_OrOp:              op1=AndOp ( 'Or'-         op2=AndOp )*;
AndOp:              op1=NotOp ( 'And'-        op2=NotOp )*;
NotOp:             opr?='Not'                 op_=CmpOp;
CmpOp:              op1=AddOp ( opr=CmpToken  op2=AddOp )*;
CaseOp:             opr=CmpToken              op_=AddOp;    // select-case operation
AddOp:              op1=ModOp ( opr=Signal    op2=ModOp )*;
ModOp:              op1=IdvOp ( 'Mod'-        op2=IdvOp )*;
IdvOp:              op1=MulOp ( '/'           op2=MulOp )*;
MulOp:              op1=NegOp ( opr=/(\*|\/)/ op2=NegOp )*;
NegOp:              opr=Signal*               op_=ExpOp;
ExpOp:              op1=_Atom ( '^'-          op2=_Atom )*;
_Atom:              Numeral | Var | '(' Expression ')'; // highest

CmpToken:           '=' | '<>' | '<=' | '<' | '>=' | '>';
Signal:             /[-+]/;
Numeral:            Fractional | Integer;
Digit:              !( /\D/ ) /[0-9]/;
Fractional:         Signal* Digit* '.' Digit*;
Integer:            Signal* Digit+ | Signal* HexPrefix HexDigit+ | Signal* OctPrefix OctDigit+ | Signal* BinPrefix BinDigit+;
HexPrefix:          '&H';
HexDigit:           /[0-9A-Fa-f]/;
OctPrefix:          '&O';
OctDigit:           /[0-7]/;
BinPrefix:          '&B';
BinDigit:           /[01]/;

EOL:                "\n";
Sep:                ':' | "\n";
StmtSep:            EOL* ':' EOL*;

Comment[ws=" \t"]:
        ( "'" | 'Rem' ) ( !( "\n" ) /[^\n]/ )* EOL;
"""

# TODO: move these to different files.
class ImpOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Imp {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class EqvOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Eqv {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class XorOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Xor {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class _OrOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Or {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class AndOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} And {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class NotOp(object):
    def __init__(self, parent, opr, op_):
        self.parent = parent
        self.opr = opr
        self.op_ = op_

    def __str__(self):
        if self.opr:
            return "(Not {})".format(self.op_)
        else:
            return "{}".format(self.op_)


class CmpOp(object):
    def __init__(self, parent, op1, opr=None, op2=None):
        self.parent = parent
        self.op1 = op1
        self.opr = opr
        self.op2 = op2

    def __str__(self):
        if self.opr:
            expr = self.op1

            for i, op2 in enumerate(self.op2):
                opr = self.opr[i]
                expr = f"({expr} {opr} {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class AddOp(object):
    def __init__(self, parent, op1, opr=None, op2=None):
        self.parent = parent
        self.op1 = op1
        self.opr = opr
        self.op2 = op2

    def __str__(self):
        if self.opr:
            expr = self.op1

            for i, op2 in enumerate(self.op2):
                opr = self.opr[i]
                expr = f"({expr} {opr} {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class ModOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} Mod {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class IdvOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = rf"({expr} \ {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class MulOp(object):
    def __init__(self, parent, op1, opr=None, op2=None):
        self.parent = parent
        self.op1 = op1
        self.opr = opr
        self.op2 = op2

    def __str__(self):
        if self.opr:
            expr = self.op1

            for i, op2 in enumerate(self.op2):
                opr = self.opr[i]
                expr = f"({expr} {opr} {op2})"

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class NegOp(object):
    def __init__(self, parent, opr, op_):
        self.parent = parent
        self.opr = opr
        self.op_ = op_

    def __str__(self):
        if self.opr:
            expr = self.op_

            for opr in self.opr:
                expr = f"({opr} {expr})"

            return "({})".format(expr)
        else:
            return "{}".format(self.op_)


class ExpOp(object):
    def __init__(self, parent, op1, op2=None):
        self.parent = parent
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        if self.op2:
            expr = self.op1

            for op2 in self.op2:
                expr = f"({expr} ^ {op2})";

            return "{}".format(expr)
        else:
            return "{}".format(self.op1)


class Expression(object):
    def __init__(self, parent, expr):
        self.parent = parent
        self.expr = expr

    def __str__(self):
        return "{}".format(self.expr)


class PrintParams(object):
    def __init__(self, parent, exprs, using):
        self.exprs = exprs
        self.using = using

    def __str__(self):
        val = ""
        for expr in self.exprs:
            val += f"{expr}";

        return val;


class PrintStmt(object):
    def __init__(self, parent, fileno, params):
        self.parent = parent
        self.fileno = fileno
        self.params = params

    def __str__(self):
        return "{} {}".format(self.fileno + ";" if self.fileno else "", self.params)


class SelectStmt(object):
    def __init__(self, parent, expr, cases):
        self.parent = parent
        self.expr = expr
        self.cases = cases

    def write(self, file):
        pass


def create_metamodel(**kwargs):
    classes = [SelectStmt, PrintStmt, PrintParams, ImpOp, EqvOp, XorOp, _OrOp, AndOp,
               NotOp, CmpOp, AddOp, ModOp, IdvOp, MulOp, NegOp, ExpOp, Expression]
    try:
        debug_mode = kwargs['debug']
    except KeyError:
        debug_mode = False
    return metamodel_from_str(grammar, classes=classes, ws=" \t", skipws=True,
                              ignore_case=True, debug=debug_mode)
