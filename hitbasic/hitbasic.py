import inspect 
import sys

from textx import metamodel_from_str, get_children_of_type
from hitbasic.models import *;


grammar = r"""
Program[ws=" \t"]:
    Sep*- statements*=AllStmtTypes[/(:|\n)+/] Sep*-;

MinStmtTypes[ws=" \t"]:
    DimStmt | ConditionalStmt | SelectStmt | DoLoopStmt | CloseStmt | OpenStmt | NextStmt | ForStmt |
    PrintStmt | BranchStmt | GraphicStmtTypes | LetStmt | DefStmt | InputStmt | PlayStmt | SwitcherStmt |
    SimpleStmt | AttrStmt; 

AllStmtTypes:
    FuncStmt | SubStmt | MinStmtTypes;

GraphicStmtTypes:
    DrawStmt | CircleStmt | ColorDefStmt | ColorStmt | CopyStmt | LineStmt | PaintStmt | PresetStmt |
    PsetStmt | PutKanjiStmt | PutSpriteStmt | ScreenStmt | SetPageStmt;

DrawStmt:           'Draw' StringExp;
CircleStmt:         'Circle' pt=StepPtArg CircleStmtArgs;
CircleStmtArgs:     ',' color=NumericExp ( ',' color=NumericExp )?;
ColorDefStmt:       'Color' '=' ( 'New' | 'Restore' | '(' Expression ',' Expression ',' Expression ',' Expression ')' );
ColorStmt:          'Color' fg=NumericExp? ( ',' bg=NumericExp? ( ',' bd=NumericExp? )? )?;
CopyStmt:           'Copy' CopySrcArg 'To' CopyDstArg;
LineStmt:           'Line' pt=StepPtArg? DstPtArg LineStmtArgs?;
LineStmtArgs:       ',' color=NumericExp ( ',' ShapeArg? ( ',' opr=OprArg? )? )?;
PaintStmt:          'Paint' pt=StepPtArg PaintStmtArgs?;
PaintStmtArgs:      ',' color=NumericExp ( ',' color=NumericExp? )?; 
PresetStmt:         'Preset' pt=StepPtArg PsetStmtArgs?;
PsetStmt:           'Pset' pt=StepPtArg PsetStmtArgs?;
PsetStmtArgs:       ',' color=NumericExp ( ',' opr=OprArg? )?;
PutKanjiStmt:       'Put' 'Kanji' pt=StepPtArg ',' jis=NumericExp ( ',' color=NumericExp? ( ',' opr=OprArg? ( ',' mode=NumericExp? )? )? )?;
PutSpriteStmt:      'Put' 'Sprite' Expression ',' pt=StepPtArg PutSpriteStmtArgs?;
PutSpriteStmtArgs:  ',' color=NumericExp ( ',' NumericExp );
ScreenStmt:         'Screen' mode=NumericExp? ( ',' spriteSize=NumericExp? ( ',' clickStatus=NumericExp? ( ',' baudRate=NumericExp?
                    ( ',' printerType=NumericExp? ( ',' interlaceMode=NumericExp? )? )? )? )? )?;
SetPageStmt:        'Set' 'Page' displayPage=NumericExp? ( ',' activePage=NumericExp )?;  
StepPtArg:          step?='Step' PtArg;
PtArg:              '(' x=NumericExp ',' y=NumericExp ')';

DstPtArg:           '-' step?='Step' PtArg;

CopySrcArg:         PtArg DstPtArg ( ',' page=NumericExp )? | Array ( ',' dir=NumericExp )? |
                    filepath=STRING ( ',' dir=NumericExp )?;
CopyDstArg:         PtArg ( ',' page=NumericExp ( ',' opr=OprArg? )? )? | filepath=STRING | Array;
OprArg:             'And' | 'Or' | 'Preset' | 'Pset' | 'Xor' | 'Tand' | 'Tor' | 'Tpreset' | 'Tpset' | 'Txor';
ShapeArg:           'BF' | 'B';

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

ConditionalStmt:    IfThenElseStmt | IfThenStmt | IfThenElseOneLiner | IfThenOneLiner;

IfExpressionThen:   !( 'Then' ) Expression 'Then'-;

IfThenElseOneLiner:
    'If' expr=IfExpressionThen thenStmts*=OneLinerStmtTypes[/:+/ eolterm]
    'Else' elseStmts*=OneLinerStmtTypes[/:+/ eolterm];

IfThenOneLiner:
    'If' expr=IfExpressionThen statements*=OneLinerStmtTypes[/:+/ eolterm];

OneLinerStmtTypes:  !( 'Else' )- MinStmtTypes;
//OneLinerStmtTypes:  !( EOL )- MinStmtTypes;

ThenClause: statements*=ThenStmtTypes[/:+/ eolterm];

EndIfClause: statements*=EndIfStmtTypes[/:+/ eolterm];

IfThenElseStmt:
    'If' expr=Expression ('Then' | Sep)? Sep* thenStmts*=ThenStmtTypes[/(:|\n)+/] Sep*
    'Else' Sep* elseStmts*=EndIfStmtTypes[/(:|\n)+/] Sep* EndIfStmt;

IfThenStmt:
    'If' expr=Expression ('Then' | Sep)? Sep* statements*=EndIfStmtTypes[/(:|\n)+/]  Sep* EndIfStmt;

EndIfStmtTypes:     !( 'End' 'If' )- MinStmtTypes;

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

PrintStmt:          ( 'Print' | '?' ) ( fileno=PrintFileNo )? params=PrintParams;
PrintFileNo:        '#' id=NumericExp ',';
PrintParams:        exprs*=PrintExprs ( using=PrintUsing )?;
PrintExprs:         Expression | /(;|,)/;
PrintUsing:         'Using' fmt=PrintUsingFmt ';' exprs+=Expression[/(,|;)/];
PrintUsingFmt:      String | Var;

BranchStmt:         'Goto' | 'Gosub';

LetStmt:            'Let';

DefStmt:            'Def Fn';

InputStmt:          'Input' args=InputArgs;
InputArgs:          InputPrompt | InputFile;
InputPrompt:        ( String ';' )? vars*=Var[/,/];
InputFile:          '#' NumericExp ',' vars*=Var[/,/];

PlayStmt:           'Play';

SwitcherStmt:       'x';

SimpleStmt[ws=' \t']:   keyword=KeywordStmt;

KeywordStmt:        'Beep' | 'Cls' | 'End' | 'Nop';

AttrStmt:           'Let'? definition=VarDefn;
VarDefn:            var=Var '=' expr=Expression;

VarType:
    'Boolean' | 'BOOL' | 'Integer' | 'INT' | 'String' | 'STR' | 'Single' | 'SNG' | 'Double' | 'DBL';

Label:              '@' Name;
Var:                Array | Identifier;
Array:              identifier=Identifier '(' ( subscripts*=NumericExp[/,/] )? ')';
Identifier:         TypedName | Name;

String[noskipws]:
    '"' /[^"]*/ '"';

TypedName:          Name TypeDescriptor;

TypeDescriptor:     /[$#!%]/;

Name:               /[_A-Za-z][_A-Za-z0-9]*/;

Expression:         NumericExp | StringExp;

StringExp:          STRING | Var;

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

# Read all classes in models
classes = {}

for module in [globals()[name] for name in modules]:
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            classes[name] = obj


def create_metamodel(**kwargs):
    try:
        debug_mode = kwargs['debug']
    except KeyError:
        debug_mode = False
    return metamodel_from_str(grammar, classes=class_provider, ws=" \t", skipws=True, ignore_case=True, debug=debug_mode)


def class_provider(name):
    global classes
    if name == 'ScreenStmt': print(name, classes.get(name))
    return classes.get(name)
