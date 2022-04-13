from textx import metamodel_from_str, get_children_of_type

grammar = """
Program:            statements*=Statements[/[:\n]*/] EOL?;
Statements:         Sep*- StmtTypes;
StmtTypes:          FunctionStmt | SubStmt | DimStmt | IfThenElseStmt | SelectStmt | DoLoopStmt | CloseStmt |
                    OpenStmt | NextStmt | ForStmt | PrintStmt | BranchStmt | ExitStmt | GraphicsStmt | LetStmt |
                    DefStmt | InputStmt | PlayStmt | SwitcherStmt | SimpleStmt | AttrStmt;

FunctionStmt:       FunctionHeader StmtSep body=FuncBody StmtSep FunctionStmtEnd;
FunctionHeader:     'blah';
FuncBody:           Statements &(StmtSep FunctionStmtEnd);
FunctionStmtEnd:    'doh';

SubStmt:            'Sub';

DimStmt:            'Dim';

IfThenElseStmt:     'If';

SelectStmt:         'Select' expr=Expression ':'- Sep+ cases*=CaseStmt SelectStmtEnd;
CaseStmt:           'Case'- expr=Expression ':'- statements*=Statements[/[:\n]*/] CaseStmtEnd-;
CaseStmtEnd:        Sep+ &( ( 'End' 'Select' | 'Case' ) );
SelectStmtEnd:      'End' 'Select' &Sep+;

DoLoopStmt:         'Do';

CloseStmt:          'Close';

OpenStmt:           'Open';

NextStmt:           'Next';

ForStmt:            'For';

PrintStmt:          'Print' num=INT;

BranchStmt:         'Goto';

ExitStmt:           'End';

GraphicsStmt:       'Graphics';

LetStmt:            'Let';

DefStmt:            'Def Fn';

InputStmt:          'Input';

PlayStmt:           'Play';

SwitcherStmt:       'x';

SimpleStmt:         'y';

AttrStmt:           'a';

Expression:         /[^:\n]+/;
EOL:                "\n";
Sep:                ':' | "\n";
StmtSep:            EOL* ':' EOL*;
Comment:            ("'" | 'Rem') !("\n") /[^\n]*/;
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
    return metamodel_from_str(grammar, classes=[Expression, SelectStmt], skipws=True, ws='\t ',
                              ignore_case=True, debug=debug_mode)
