from textx import metamodel_from_str, get_children_of_type

grammar = """
Program:            statements=Statements EOL?;
Statements:         Sep* contents*=StmtTypes[/[:\n]*/];
StmtTypes:          FunctionStmt | SubStmt | DimStmt | IfThenElseStmt | SelectStmt | DoLoopStmt | CloseStmt |
                    OpenStmt | NextStmt | ForStmt | PrintStmt | BranchStmt | ExitStmt | GraphicsStmt | LetStmt |
                    DefStmt | InputStmt | PlayStmt | SwitcherStmt | ParamlessStmt | AttrStmt;

FunctionStmt:       'Function';

SubStmt:            'Sub';

DimStmt:            'Dim';

IfThenElseStmt:     'If';

SelectStmt:         'Select' expr=Expression ':' Sep cases*=CaseStmt SelectStmtEnd;
Expression:         /[^:]+/;
CaseStmt:           'Case' expr=Expression ':' statements=Statements CaseStmtEnd;
CaseStmtEnd:        Sep+ &( ( 'End' 'Select' | 'Case' ) );
SelectStmtEnd:      'End' 'Select' &Sep;

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

SwitcherStmt:       ;

NoParamStmt:        ;

AttrStmt:           ;

Sep:                ':' | "\n";
EOL:                "\n";
Comment:            ("'" | 'Rem') !("\n") /[^\n]*/;
"""

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


# Create meta-model from the grammar.
mm = metamodel_from_str(grammar, classes=[Expression, SelectStmt], skipws=True, ws='\t ', ignore_case=True, debug=True)

source_code = """
    Print 3 ::: Print 1
    Select xpto:
        Case bla:
           Print 7 :
        Case bla2:
           Print 8 : Print 9
    End Select
    Print 4: Print 2 :::::
    Print 10
"""

# Meta-model knows how to parse and instantiate models.
program = mm.model_from_str(source_code)

# At this point model is a plain Python object graph with instances of
# dynamically created classes and attributes following the grammar.

def cname(o):
    return o.__class__.__name__

# Let's interpret the program 
#statements = [program.statements.head] + program.statements.tail;

with file as open('./teste.out', w):
    for statement in program.statements.contents:
        if cname(statement) == 'PrintStmt':
            print('Print', statement.num)
        elif cname(statement) == 'SelectStmt':
            statement.write(file)
