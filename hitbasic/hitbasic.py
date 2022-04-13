from textx import metamodel_from_str, get_children_of_type

grammar = """
Program[ws=" \t"]:
    Sep*- statements*=AllStmtTypes[/(:|\n)+/] Sep*-;

MinStmtTypes[ws=" \t"]:
    DimStmt | IfThenElseStmt | IfThenStmt | SelectStmt | DoLoopStmt | CloseStmt | OpenStmt | NextStmt |
    ForStmt | PrintStmt | BranchStmt | GraphicsStmt | LetStmt | DefStmt | InputStmt | PlayStmt |
    SwitcherStmt | SimpleStmt | AttrStmt; 

AllStmtTypes:
    FuncStmt | SubStmt | MinStmtTypes;

FuncStmt[ws=" \t\n"]:
    header=FuncHeads Sep*- body*=FuncStmtTypes[/(:|\n)+/] Sep*- FuncStmtEnd;

FuncHeads:          FuncHead | FuncHeadTyped;

FuncHead:           'Function' name=Name '(' params*=FuncVarDecl[/(,|\n)+/] ')' return=FuncReturnType;

FuncHeadTyped:      'Function' TypedName '(' params*=FuncVarDecl[/(,|\n)+/] ')';

FuncVarDecl:        Name 'As' VarType | TypedName;

FuncStmtTypes[ws=" \t"]:
    !('End' 'Function')- (ReturnStmt | MinStmtTypes);

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

DimVar:             name=Name ('(' ranges*=DimRangeExpr[/,/] ')')?;

DimRangeExpr:       Expression 'To' Expression | Expression;

DimAttr:            Expression | '{' Expression '}';

IfThenElseStmt[ws=" \t\n"]:
    'If' expr=Expression 'Then' ThenClause 'Else' ElseClause EndIfStmt;

IfThenStmt:
    'If' expr=Expression 'Then' ThenClause EndIfStmt;

ThenClause: statements*=ThenClauseTypes[/(:|\n)+/];

ThenClauseTypes[ws=" \t"]: !('End' 'If' | 'Else')- MinStmtTypes;

ElseClause: statements*=ElseClauseTypes[/(:|\n)+/];

ElseClauseTypes[ws=" \t"]: !('End' 'If')- MinStmtTypes;

EndIfStmt:          'End' 'If' &Sep+;

SelectStmt:
    'Select' expr=Expression Sep*- cases*=CaseStmtTypes[/(:|\n)+/] Sep*- SelectStmtEnd;

CaseStmtTypes:      !('End' 'Select')- (CaseStmt | MinStmtTypes);

CaseStmt[ws=' \t\n']:
    'Case'- ('Else' | expr=Expression);

SelectStmtEnd:      'End' 'Select' &Sep+;

DoLoopStmt:         'Do';

CloseStmt:          'Close';

OpenStmt:           'Open';

NextStmt:           'Next';

ForStmt:            'For';

PrintStmt[ws=' \t\n']:
    'Print' num?=INT;

BranchStmt:         'Goto';

ExitStmt:           'XEnd';

GraphicsStmt:       'Graphics';

LetStmt:            'Let';

DefStmt:            'Def Fn';

InputStmt:          'Input';

PlayStmt:           'Play';

SwitcherStmt:       'x';

SimpleStmt[ws=' \t\n']:
    keyword=KeywordStmt;

KeywordStmt:        'Beep' | 'Cls' | 'End' | 'Nop';

AttrStmt:           'a';

VarType:
    'Boolean' | 'BOOL' | 'Integer' | 'INT' | 'String' | 'STR' | 'Single' | 'SNG' | 'Double' | 'DBL';

Label:              '@' Name;

Identifier:         TypedName | Name;

TypedName:          Name TypeDescriptor;

TypeDescriptor:     /[$#!%]/;

Name:               /[_A-Za-z][_A-Za-z0-9]*/;

Expression:         /[^,:\n]+/;
EOL:                "\n";
Sep:                ':' | "\n";
StmtSep:            EOL* ':' EOL*;

Comment[ws=" \t"]:
        ("'" | 'Rem') (!("\n") /[^\n]/)* "\n";
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
