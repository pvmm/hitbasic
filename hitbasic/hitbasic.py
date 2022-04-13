from textx import metamodel_from_str, get_children_of_type

grammar = """
Program[ws=" \t"]:
        Sep*- statements*=AllStmtTypes[/(:|\n)+/] Sep*-;

MinStmtTypes:
        DimStmt | IfThenElseStmt | SelectStmt | DoLoopStmt | CloseStmt | OpenStmt | NextStmt | ForStmt |
        PrintStmt | BranchStmt | ExitStmt | GraphicsStmt | LetStmt | DefStmt | InputStmt | PlayStmt |
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

DimStmt:            'Dim';

IfThenElseStmt:     'If';

SelectStmt:         'Select' expr=Expression ':' Sep*- cases*=CaseStmtTypes[/(:|\n)+/] Sep*- SelectStmtEnd;

CaseStmtTypes:      !('End' 'Select')- (CaseStmt | MinStmtTypes);

CaseStmt:           'Case'- expr=Expression ':';

SelectStmtEnd:      'End' 'Select' &Sep+;

DoLoopStmt:         'Do';

CloseStmt:          'Close';

OpenStmt:           'Open';

NextStmt:           'Next';

ForStmt:            'For';

PrintStmt:          'Print' num=INT;

BranchStmt:         'Goto';

ExitStmt:           'XEnd';

GraphicsStmt:       'Graphics';

LetStmt:            'Let';

DefStmt:            'Def Fn';

InputStmt:          'Input';

PlayStmt:           'Play';

SwitcherStmt:       'x';

SimpleStmt:         'y';

AttrStmt:           'a';

VarType:
        'Boolean' | 'BOOL' | 'Integer' | 'INT' | 'String' | 'STR' | 'Single' | 'SNG' | 'Double' | 'DBL';

Label:              '@' Name;

Identifier:         TypedName | Name;

TypedName:          Name TypeDescriptor;

TypeDescriptor:     /[$#!%]/;

Name:               /[_A-Za-z][_A-Za-z0-9]+/;

Expression:         /[^:\n]+/;
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
