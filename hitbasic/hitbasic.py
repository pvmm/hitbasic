from textx import metamodel_from_str, get_children_of_type

grammar = """
Program[ws=" \t"]:
    Sep*- statements*=AllStmtTypes[/(:|\n)+/] Sep*-;

MinStmtTypes[ws=" \t"]:
    DimStmt | ConditionalStmt | SelectStmt | DoLoopStmt | CloseStmt | OpenStmt | NextStmt | ForStmt |
    PrintStmt | BranchStmt | GraphicsStmt | LetStmt | DefStmt | InputStmt | PlayStmt | SwitcherStmt |
    SimpleStmt | AttrStmt; 

AllStmtTypes:
    FuncStmt | SubStmt | MinStmtTypes;

FuncStmt[ws=" \t\n"]:
    header=FuncHeads Sep*- body*=FuncStmtTypes[/(:|\n)+/] Sep*- FuncStmtEnd;

FuncHeads:          FuncHead | FuncHeadTyped;

FuncHead:           'Function' name=Name '(' params*=FuncVarDecl[/(,|\n)+/] ')' return=FuncReturnType;

FuncHeadTyped:      'Function' TypedName '(' params*=FuncVarDecl[/(,|\n)+/] ')';

FuncVarDecl:        Name 'As' VarType | TypedName;

FuncStmtTypes[ws=" \t"]:
    !('End' 'Function')- ( ReturnStmt | MinStmtTypes );

ReturnStmt:         'Return' Identifier;

FuncReturnType:     'As' VarType;

FuncStmtEnd:        'End' 'Function';

SubStmt:            'Sub';

DimStmt[ws=' \t\n']:
    'Dim' vars+=DimVarDecl[/,/];

DimVarDecl:         DimVar 'As' VarType '=' DimAttr |
                    DimVar 'As' VarType |
                    DimVar '=' DimAttr |
                    DimVar;

DimVar:             name=Name ( '(' ranges*=DimRangeExpr[/,/] ')' )?;

DimRangeExpr:       Expression 'To' Expression | Expression;

DimAttr:            Expression | '{' Expression '}';

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
    'If' expr=IfExpressionThen 'Then'? Sep? ThenBlock Sep? 'Else' Sep? EndIfBlock EndIfStmt &Sep;

IfThenStmt:
    'If' expr=IfExpressionThen 'Then'? Sep? EndIfBlock Sep? EndIfStmt &Sep;

ThenBlock[ws=' \t\n']: statements*=ThenStmtTypes[/\n+/];

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

DoLoopStmt:         'Do';

CloseStmt:          'Close';

OpenStmt:           'Open';

NextStmt:           'Next';

ForStmt:            'For';

PrintStmt[ws=' \t\n']:
    ('Print' | '?') ( fileno=PrintFileNo )? params=PrintParams;

PrintFileNo:        '#' Expression ',';

PrintParams:        exprs*=Expression[/(,|;)/] ( using=PrintUsing )?;

PrintUsing:         'Using' fmt=PrintUsingFmt ';' exprs+=Expression[/(,|;)/];

PrintUsingFmt:      String | Identifier;

BranchStmt:         'Goto' | 'Gosub';

GraphicsStmt:       'Graphics';

LetStmt:            'Let';

DefStmt:            'Def Fn';

InputStmt:          'Input';

PlayStmt:           'Play';

SwitcherStmt:       'x';

SimpleStmt[ws=' \t\n']:
    keyword=KeywordStmt;

KeywordStmt:        'Beep' | 'Cls' | 'End' | 'Nop';

AttrStmt:           'a=b';

VarType:
    'Boolean' | 'BOOL' | 'Integer' | 'INT' | 'String' | 'STR' | 'Single' | 'SNG' | 'Double' | 'DBL';

Label:              '@' Name;

Identifier:         TypedName | Name;

String[noskipws]:
    '"' /[^"]*/ '"';

TypedName:          Name TypeDescriptor;

TypeDescriptor:     /[$#!%]/;

Name:               /[_A-Za-z][_A-Za-z0-9]*/;

Expression:         /[^, :\n]+/;
EOL:                "\n";
Sep:                ':' | "\n";
StmtSep:            EOL* ':' EOL*;

Comment[ws=" \t"]:
        ("'" | 'Rem') (!("\n") /[^\n]/)* EOL;
"""

# TODO: move these to different files.
class Expression(object):
    def __init__(self, parent, expr):
        self.parent = parent
        self.expr = expr

    def __str__(self):
        return "{}".format(self.expr)


class SelectStmt(object):
    def __init__(self, parent, expr, cases):
        self.parent = parent
        self.expr = expr
        self.cases = cases

    def write(self, file):
        pass


def create_metamodel(**kwargs):
    try:
        debug_mode = kwargs['debug']
    except KeyError:
        debug_mode = False
    return metamodel_from_str(grammar, classes=[Expression, SelectStmt], ws=" \t", skipws=True,
                              ignore_case=True, debug=debug_mode)
