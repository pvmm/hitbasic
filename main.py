from textx import metamodel_from_str, get_children_of_type

grammar = """
Program:     statements=Statements EOL?;
Statements:  Sep* contents*=StmtTypes[/[:\n]*/];
StmtTypes:   SelectCase | PrintStmt;
SelectCase:  'Select' expr=Expression ':' Sep cases*=CaseStmt SlctCaseEnd;
Expression:  /[^:]+/;
CaseStmt:    'Case' expr=Expression ':' statements=Statements CaseStmtEnd;
CaseStmtEnd:  Sep+ &( ( 'End' 'Select' | 'Case' ) );
SlctCaseEnd: 'End' 'Select' &Sep;
PrintStmt:   'Print' num=INT;
Sep:         ':' | "\n";
EOL:         "\n";
Comment:     ("'" | 'Rem') !("\n") /[^\n]*/;
"""

# Classes for other rules will be dynamically generated.
class Expression(object):
    def __init__(self, parent, expr):
        self.parent = parent
        self.expr = expr

    def __str__(self):
        return "{}".format(self.expr)

# Create meta-model from the grammar.
mm = metamodel_from_str(grammar, classes=[Expression], skipws=True, ws='\t ', ignore_case=True, debug=True)

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

for statement in program.statements.contents:
    #statement = statement.content;
    #print('{}: {}.'.format(cname(statement), statement))
    if cname(statement) == 'PrintStmt':
        print('Print', statement.num)
    elif cname(statement) == 'SelectCase':
        print('Select', statement.expr)
        print('Select', statement.cases)

