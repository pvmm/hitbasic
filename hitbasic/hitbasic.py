import inspect 
import sys

from textx import metamodel_from_str, get_children_of_type

from hitbasic.models import *
from hitbasic.symbol_table import SymbolTable
from hitbasic.models import create_processors


grammar = r"""
Program[ws=" \t"]:  Sep*- statements*=Statements[/(:|\n)+/] Sep*-;

Statements:         Sep?- ( ( LabelMark Sep?- AllStmtTypes ) | AllStmtTypes | LabelMark )*;

AllStmtTypes:       FuncStmt | SubStmt | MinStmtTypes;

MinStmtTypes:
    ConstStmt | DimStmt | ConditionalStmt | SelectStmt | DoLoopStmt | CloseStmt | OpenStmt | NextStmt | ForStmt |
    PrintStmt | BranchStmt | GraphicStmtTypes | LetStmt | DefStmt | InputStmt | DataStmt | ReadStmt | PlayStmt | SwitcherStmt |
    SimpleStmt | AssignStmt;

GraphicStmtTypes:
    DrawStmt | CircleStmt | ColorDefStmt | ColorStmt | CopyStmt | LineStmt | PaintStmt | PresetStmt |
    PsetStmt | PutKanjiStmt | PutSpriteStmt | ScreenStmt | SetPageStmt;

DrawStmt:           'Draw' Expression;
CircleStmt:         'Circle' pt=StepPtArg CircleStmtArgs;
CircleStmtArgs:     ',' color=Expression ( ',' color=Expression )?;
ColorDefStmt:       'Color' '=' ( 'New' | 'Restore' | '(' Expression ',' Expression ',' Expression ',' Expression ')' );
ColorStmt:          'Color' fg=Expression? ( ',' bg=Expression? ( ',' bd=Expression? )? )?;
CopyStmt:           'Copy' CopySrcArg 'To' CopyDstArg;
LineStmt:           'Line' src=StepPtArg? '-' dst=StepPtArg args=LineStmtArgs?;
LineStmtArgs:       ',' color=Expression? ( ',' shape=ShapeArg? ( ',' opr=OprArg? )? )?;
PaintStmt:          'Paint' pt=StepPtArg args=PaintStmtArgs?;
PaintStmtArgs:      ',' color=Expression ( ',' color=Expression? )?; 
PresetStmt:         'Preset' pt=StepPtArg args=PsetStmtArgs?;
PsetStmt:           'Pset' pt=StepPtArg args=PsetStmtArgs?;
PsetStmtArgs:       ',' color=Expression ( ',' opr=OprArg? )?;
PutKanjiStmt:       'Put' 'Kanji' pt=StepPtArg ',' jis=Expression ( ',' color=Expression? ( ',' opr=OprArg? ( ',' mode=Expression? )? )? )?;
PutSpriteStmt:      'Put' 'Sprite' Expression ',' pt=StepPtArg args=PutSpriteStmtArgs?;
PutSpriteStmtArgs:  ',' color=Expression ( ',' Expression );
ScreenStmt:         'Screen' mode=Expression? ( ',' spriteSize=Expression? ( ',' clickStatus=Expression? ( ',' baudRate=Expression?
                    ( ',' printerType=Expression? ( ',' interlaceMode=Expression? )? )? )? )? )?;
SetPageStmt:        'Set' 'Page' displayPage=Expression? ( ',' activePage=Expression )?;  
StepPtArg:          step?='Step' coor=PtArg;
PtArg:              '(' x=Expression ',' y=Expression ')';

CopySrcArg:         PtArg '-' StepPtArg ( ',' page=Expression )? | Array ( ',' dir=Expression )? |
                    filepath=STRING ( ',' dir=Expression )?;
CopyDstArg:         PtArg ( ',' page=Expression ( ',' opr=OprArg? )? )? | filepath=STRING | Array;
OprArg:             'And' | 'Or' | 'Preset' | 'Pset' | 'Xor' | 'Tand' | 'Tor' | 'Tpreset' | 'Tpset' | 'Txor';
ShapeArg:           'BF' | 'B';

LabelMark:          &( /^[0-9@]/ ) ( identifier=Label? | line_num=Integer? );

FuncStmt:           header=FuncHeads Sep*- statements*=FuncStmtTypes[/(:|\n)+/] Sep*- FuncStmtEnd;
FuncHeads:          FuncHead | FuncHeadTyped;
FuncHead:           'Function' identifier=Name '(' params*=FuncParam[/(,|\n)+/] ')' ret=FuncReturnType;
FuncHeadTyped:      'Function' identifier=TypedName '(' params*=FuncParam[/(,|\n)+/] ')';
FuncParam:          identifier=Name 'As' type=VarType | name=TypedName;
FuncStmtTypes:      !('End' 'Function')- ( FuncExitStmt | ReturnStmt | MinStmtTypes );
FuncExitStmt:       'Exit' 'Function';
ReturnStmt:         'Return' ( expr=Expression | target=Label? );
FuncReturnType:     'As'- type=VarType;
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

DimStmt[ws=' \t\n']: 'Dim' declarations+=DimVarDecl[/,/];

DimVarDecl:         ( var=DimScalar | var=DimArray 'As' type=VarType ) '=' expr=Expression |
                    ( var=DimScalar | var=DimArray 'As' type=VarType ) |
                    ( var=DimScalar | var=DimArray ) '=' expr=Expression |
                    ( var=DimScalar | var=DimArray );

DimScalar:          identifier=TypedName;
DimArray:           identifier=Name ( '(' ranges*=DimRangeDecl[/,/] ')' )?;

DimRangeDecl:       begin=Expression 'To' end=Expression | end=Expression;

ConditionalStmt:    IfThenElseStmt | IfThenStmt | IfThenElseOneLiner | IfThenOneLiner;

IfExpressionThen:   !( 'Then' ) Expression 'Then'-;

IfThenElseOneLiner:
    'If' expr=IfExpressionThen then_stmts*=OneLinerStmtTypes[/:+/ eolterm]
    'Else' else_stmts*=OneLinerStmtTypes[/:+/ eolterm];

IfThenOneLiner:
    'If' expr=IfExpressionThen statements*=OneLinerStmtTypes[/:+/ eolterm];

OneLinerStmtTypes:  !( 'Else' )- MinStmtTypes;
//OneLinerStmtTypes:  !( EOL )- MinStmtTypes;

ThenClause: statements*=ThenStmtTypes[/:+/ eolterm];

EndIfClause: statements*=EndIfStmtTypes[/:+/ eolterm];

IfThenElseStmt:
    'If' expr=Expression ('Then' | Sep)? Sep* then_stmts*=ThenStmtTypes[/(:|\n)+/] Sep*-
    'Else' Sep*- else_stmts*=EndIfStmtTypes[/(:|\n)+/] Sep*- EndIfStmt;

IfThenStmt:         'If' expr=Expression ('Then' | Sep)? Sep*- statements*=EndIfStmtTypes[/(:|\n)+/] Sep*- EndIfStmt;

EndIfStmtTypes:     !( 'End' 'If' )- MinStmtTypes;

ThenStmtTypes:      !( 'Else' )- MinStmtTypes;

EndIfStmt:          'End' 'If' &Sep+-;

SelectStmt:         'Select' expr=Expression Sep+- ( cases+=CaseClause | Sep+- )? SelectStmtEnd;
CaseClause:         'Case' expr=CaseExpr Sep+- statements*=CaseStmtTypes[/(:|\n)+/] Sep+- CaseClauseEnd;
CaseExpr:           else_clause?='Else' | 'Is' is_clause=CaseCmpOp | expr=Expression;
//CaseStmtTypes:      !( 'End' 'Select' )- ( CaseClause | MinStmtTypes );
CaseStmtTypes:      !( 'End' 'Select' )- MinStmtTypes;
CaseClauseEnd:      &( 'End' 'Select' | 'Case' );
SelectStmtEnd:      'End' 'Select';

DoLoopStmt:         'Do' condition=DoCond Sep+- statements*=DoStmtTypes[/(:|\n)+/] Sep*- 'Loop' |
                    'Do' Sep+- statements*=DoStmtTypes[/(:|\n)+/] Sep*- 'Loop' condition=DoCond;
DoCond:             ( 'While' | 'Until' ) expr=Expression;
DoStmtTypes:        !( 'Loop' )- ( ExitDoStmt | MinStmtTypes );
ExitDoStmt:         'Exit' 'Do';

CloseStmt:          'Close' Fileno;
Fileno:             '#' Expression;

OpenStmt:           'Open';

NextStmt:           'Next' ( vars*=Var[/,/] )?;

ForStmt:            'For' var=Var '=' range=ForRangeDecl;
ForRangeDecl:       begin=Expression 'to'- end=Expression ( 'Step'- step=Expression )?;

PrintStmt:          ( 'Print' | '?' ) ( fileno=PrintFileNo )? params=PrintParams;
PrintFileNo:        '#' id=Expression ',';
PrintParams:        expressions*=PrintExpr ( using=PrintUsing )?;
PrintExpr:          expr=Expression | sep=/[;,]/;
PrintUsing:         'Using' fmt=PrintUsingFmt ';' expressions+=Expression[/(,|;)/];
PrintUsingFmt:      String | RValue;

BranchStmt:         stmt=BranchType param=Address;
BranchType:         'Goto' | 'Gosub' | 'Restore';
Address:            Label | Integer;

LetStmt:            'Let' vars+=LetVarDecl[/,/];
LetVarDecl:         ( id=TypedName | id=Name 'As' VarType ) '=' expr=Expression |
                    ( id=TypedName | id=Name ) '=' expr=Expression;

DefStmt:            'Def' 'Fn';

InputStmt:          'Input' args=InputArgs;
InputArgs:          InputPrompt | InputFile;
InputPrompt:        ( String ';' )? vars+=Var[/,/];
InputFile:          '#' Expression ',' vars*=Var[/,/];

DataStmt:           'Data' ctnt*=DataContent[/,/];
DataContent:        String | Numeral;

ReadStmt:           'Read' vars+=Var[/,/];

PlayStmt:           'Play';

SwitcherStmt:       'x';

SimpleStmt:         keyword=KeywordStmt;

KeywordStmt:        'Beep' | 'Cls' | 'End' | 'Nop';

AssignStmt:         'Let'? definition=VarDefn;
VarDefn:            var=LValue '=' expr=Expression;

VarType:            'Boolean' | 'BOOL' | 'Integer' | 'INT' | 'String' | 'STR' | 'Single' | 'SNG' | 'Double' | 'DBL';

LValue:             var=Var;
RValue:             var=Var;
Var:                Array | Scalar;
Array:              identifier=Identifier '(' ( params*=Expression[/,/] )? ')';
Scalar:             identifier=Identifier;
Identifier:         TypedName | Name;
Label:              '@' Name;

String[noskipws]:   ' '*- '"'- /[^"]/* '"'-;

TypedName:          Name TypeDescriptor;

TypeDescriptor:     /[$#!%]/;

Name:               /[_A-Za-z][_A-Za-z0-9]*/;

Expression:         expr=ImpOp; // Imp: lowest precedence operator
ImpOp:              op1=EqvOp ( opr='Imp'     op2=EqvOp )*;
EqvOp:              op1=XorOp ( opr='Eqv'     op2=XorOp )*;
XorOp:              op1=_OrOp ( opr='Xor'     op2=_OrOp )*;
_OrOp:              op1=AndOp ( opr='Or'      op2=AndOp )*;
AndOp:              op1=NotOp ( opr='And'     op2=NotOp )*;
NotOp:              opr='Not'*                op1=CmpOp;
CmpOp:              op1=AddOp ( opr=CmpToken  op2=AddOp )*;
CaseCmpOp:          opr=CmpToken              op1=AddOp;    // select-case operation
AddOp:              op1=ModOp ( opr=Signal    op2=ModOp )*;
ModOp:              op1=IdvOp ( opr='Mod'     op2=IdvOp )*;
IdvOp:              op1=MulOp ( opr='/'       op2=MulOp )*;
MulOp:              op1=NegOp ( opr=/(\*|\/)/ op2=NegOp )*;
NegOp:              opr=Signal*               op1=ExpOp;
ExpOp:              op1=_Atom ( opr='^'       op2=_Atom )*;
_Atom:              quoted=String | rvalue=RValue | '(' guarded=Expression ')' | num=Numeral; // highest

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


def create_metamodel(use_processor = True, **kwargs):
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
    return classes.get(name)
