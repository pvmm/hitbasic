import inspect 
import sys

from textx import metamodel_from_str, get_children_of_type

from hitbasic.models import *
from hitbasic.symbol_table import SymbolTable
from hitbasic.models import create_processors


grammar = r"""
Program[ws=" \t"]:
    Sep*- statements*=Statements[/(:|\n)+/] Sep*-;

Statements:
    Sep?- ( ( LabelMark Sep?- AllStmtTypes ) | AllStmtTypes | LabelMark )*;

AllStmtTypes:
    FuncStmt | SubStmt | MinStmtTypes;

MinStmtTypes:
    ConstStmt | DimStmt | ConditionalStmt | SelectStmt | DoLoopStmt | CloseStmt | OpenStmt | NextStmt | ForStmt |
    PrintStmt | BranchStmt | GraphicStmtTypes | LetStmt | DefStmt | InputStmt | DataStmt | ReadStmt | PlayStmt | SwitcherStmt |
    SimpleStmt | AttrStmt;

GraphicStmtTypes:
    DrawStmt | CircleStmt | ColorDefStmt | ColorStmt | CopyStmt | LineStmt | PaintStmt | PresetStmt |
    PsetStmt | PutKanjiStmt | PutSpriteStmt | ScreenStmt | SetPageStmt;

DrawStmt:           'Draw' StringExp;
CircleStmt:         'Circle' pt=StepPtArg CircleStmtArgs;
CircleStmtArgs:     ',' color=NumericExp ( ',' color=NumericExp )?;
ColorDefStmt:       'Color' '=' ( 'New' | 'Restore' | '(' Expression ',' Expression ',' Expression ',' Expression ')' );
ColorStmt:          'Color' fg=NumericExp? ( ',' bg=NumericExp? ( ',' bd=NumericExp? )? )?;
CopyStmt:           'Copy' CopySrcArg 'To' CopyDstArg;
LineStmt:           'Line' src=StepPtArg? '-' dst=StepPtArg args=LineStmtArgs?;
LineStmtArgs:       ',' color=NumericExp? ( ',' shape=ShapeArg? ( ',' opr=OprArg? )? )?;
PaintStmt:          'Paint' pt=StepPtArg args=PaintStmtArgs?;
PaintStmtArgs:      ',' color=NumericExp ( ',' color=NumericExp? )?; 
PresetStmt:         'Preset' pt=StepPtArg args=PsetStmtArgs?;
PsetStmt:           'Pset' pt=StepPtArg args=PsetStmtArgs?;
PsetStmtArgs:       ',' color=NumericExp ( ',' opr=OprArg? )?;
PutKanjiStmt:       'Put' 'Kanji' pt=StepPtArg ',' jis=NumericExp ( ',' color=NumericExp? ( ',' opr=OprArg? ( ',' mode=NumericExp? )? )? )?;
PutSpriteStmt:      'Put' 'Sprite' Expression ',' pt=StepPtArg args=PutSpriteStmtArgs?;
PutSpriteStmtArgs:  ',' color=NumericExp ( ',' NumericExp );
ScreenStmt:         'Screen' mode=NumericExp? ( ',' spriteSize=NumericExp? ( ',' clickStatus=NumericExp? ( ',' baudRate=NumericExp?
                    ( ',' printerType=NumericExp? ( ',' interlaceMode=NumericExp? )? )? )? )? )?;
SetPageStmt:        'Set' 'Page' displayPage=NumericExp? ( ',' activePage=NumericExp )?;  
StepPtArg:          step?='Step' coor=PtArg;
PtArg:              '(' x=NumericExp ',' y=NumericExp ')';

CopySrcArg:         PtArg '-' StepPtArg ( ',' page=NumericExp )? | Array ( ',' dir=NumericExp )? |
                    filepath=STRING ( ',' dir=NumericExp )?;
CopyDstArg:         PtArg ( ',' page=NumericExp ( ',' opr=OprArg? )? )? | filepath=STRING | Array;
OprArg:             'And' | 'Or' | 'Preset' | 'Pset' | 'Xor' | 'Tand' | 'Tor' | 'Tpreset' | 'Tpset' | 'Txor';
ShapeArg:           'BF' | 'B';

LabelMark:          &( /^[0-9@]/ ) ( identifier=Label? | line_num=Integer? );

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

ConstStmt:          'Const' vars+=ConstVarDecl[/,/];
ConstVarDecl:       ( id=TypedName | id=Name 'As' VarType ) '=' expr=Expression |
                    ( id=TypedName | id=Name ) '=' expr=Expression;

DimStmt[ws=' \t\n']:
    'Dim' vars+=DimVarDecl[/,/];

DimVarDecl:         ( id=TypedName | id=DimVar 'As' type=VarType ) '=' expr=Expression |
                    ( id=TypedName | id=DimVar 'As' type=VarType ) |
                    ( id=TypedName | id=DimVar ) '=' expr=Expression |
                    ( id=TypedName | id=DimVar );

DimVar:             name=Name ( '(' ranges*=DimRangeDecl[/,/] ')' )?;

DimRangeDecl:       NumericExp 'To' NumericExp | NumericExp;

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
    'If' expr=Expression ('Then' | Sep)? Sep* thenStmts*=ThenStmtTypes[/(:|\n)+/] Sep*-
    'Else' Sep*- elseStmts*=EndIfStmtTypes[/(:|\n)+/] Sep*- EndIfStmt;

IfThenStmt:
    'If' expr=Expression ('Then' | Sep)? Sep*- statements*=EndIfStmtTypes[/(:|\n)+/] Sep*- EndIfStmt;

EndIfStmtTypes:     !( 'End' 'If' )- MinStmtTypes;

ThenStmtTypes:      !( 'Else' )- MinStmtTypes;

EndIfStmt:          'End' 'If' &Sep+-;

SelectStmt:
    'Select' expr=Expression Sep*- cases*=CaseStmtTypes[/(:|\n)+/] Sep*- SelectStmtEnd;

CaseStmtTypes:      !( 'End' 'Select' )- ( CaseStmt | MinStmtTypes );

CaseStmt[ws=' \t\n']:
    'Case'- ( 'Else' | expr=Expression );

SelectStmtEnd:      'End' 'Select' &Sep+-;

DoLoopStmt:         'Do' condition=DoCond Sep+- statements*=DoStmtTypes[/(:|\n)+/] Sep*- 'Loop' |
                    'Do' Sep+- statements*=DoStmtTypes[/(:|\n)+/] Sep*- 'Loop' condition=DoCond;
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

BranchStmt:         stmt=BranchType param=Address;
BranchType:         'Goto' | 'Gosub' | 'Restore';
Address:            Label | Integer;

LetStmt:            'Let' vars+=LetVarDecl[/,/];
LetVarDecl:         ( id=TypedName | id=Name 'As' VarType ) '=' expr=Expression |
                    ( id=TypedName | id=Name ) '=' expr=Expression;

DefStmt:            'Def Fn';

InputStmt:          'Input' args=InputArgs;
InputArgs:          InputPrompt | InputFile;
InputPrompt:        ( String ';' )? vars+=Var[/,/];
InputFile:          '#' NumericExp ',' vars*=Var[/,/];

DataStmt:           'Data' ctnt*=DataContent[/,/];
DataContent:        String | Numeral;

ReadStmt:           'Read' vars+=Var[/,/];

PlayStmt:           'Play';

SwitcherStmt:       'x';

SimpleStmt:         keyword=KeywordStmt;

KeywordStmt:        'Beep' | 'Cls' | 'End' | 'Nop';

AttrStmt:           'Let'? definition=VarDefn;
VarDefn:            var=Var '=' expr=Expression;

VarType:
    'Boolean' | 'BOOL' | 'Integer' | 'INT' | 'String' | 'STR' | 'Single' | 'SNG' | 'Double' | 'DBL';

RValue:             Identifier '(' ( args*=Expression[/,/] )? ')' | Array | Identifier;
Var:                Array | Identifier;
Array:              identifier=Identifier '(' ( subscripts*=NumericExp[/,/] )? ')';
Identifier:         TypedName | Name;
Label:              '@' Name;

String[noskipws]:
    '"' /[^"]*/ '"';

TypedName:          Name TypeDescriptor;

TypeDescriptor:     /[$#!%]/;

Name:               /[_A-Za-z][_A-Za-z0-9]*/;

Expression:         NumericExp | StringExp;

StringExp:          ( Var | STRING ) '+' ( Var | STRING ) | Var | STRING;

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
_Atom:              RValue | '(' Expression ')' | Numeral; // highest

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


Comment: MultilineComments | LineComments;
MultilineComments[ws=" \t\n"]:
        '/*' ( !('*/') /./ )* '*/';
LineComments[ws=" \t"]:
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

    symbol_table = SymbolTable()
    mm = metamodel_from_str(grammar, classes=class_provider, ws=" \t", skipws=True, ignore_case=True, debug=debug_mode)
    mm.register_obj_processors(create_processors(symbol_table))
    return mm


def class_provider(name):
    global classes
    if name == 'ScreenStmt': print(name, classes.get(name))
    return classes.get(name)
