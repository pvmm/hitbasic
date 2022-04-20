#!/usr/bin/env python3

import os
import sys
import argparse
import textwrap
import shutil

from hitbasic import hitbasic
from hitbasic.generators import ascii_file


def create_model(metamodel, source, graphviz=False):
    model = mm.model_from_str(source)

    if graphviz:
        os.system('dot -Tpdf Model_parse_tree.dot -o Model_parse_tree.pdf')
        #os.system('dot -Tpdf Program_parser_model.dot -o Program_parser_model.pdf')
        #os.system('dot -Tpdf textx_model_parser_model.dot -o textx_model_parser_model.pdf')
        #os.system('dot -Tpdf textx_model_parse_tree.dot -o textx_model_parse_tree.pdf')

    return model


if __name__ == '__main__':
    argp = argparse.ArgumentParser(prog='hb', description='HitBasic transpiles high level Visual Basic like language into MSX-BASIC.',
            epilog="For bug report, suggestions, praises or complains, please go to: <https://github.com/pvmm/hitbasic>.")

    group1 = argp.add_mutually_exclusive_group(required=True)
    group1.add_argument('--version', action='store_true', required=False, help='display version and finishes')
    group1.add_argument('-x', action='store_true', required=False, help='test special case')
    group1.add_argument('-c', metavar='.ASC infile', nargs='+', type=argparse.FileType('r'), help='compile source from infile(s)')
    group1.add_argument('-s', '--stdin', action='store_true', required=False, help='transpile to MSX-BASIC program from standard input')
    group2 = argp.add_argument_group('override default configuration')
    group2.add_argument('-o', '--output', metavar='outfile', default='out.asc', type=str, help='write into outfile (default: out.asc)')
    group2.add_argument('-p', '--pretty-print', action='store_false', required=False, help='generate code in pretty-print version (default)')
    group2.add_argument('-d', '--debug', action='store_true', required=False, help='raise exception all the way up if it happens (for debugging)')
    group2.add_argument('-g', '--graphviz', action='store_true', required=False, help='generate Graphviz files program_parse_tree.dot and program_parser_model.dot')
    group2.add_argument('-b', '--begin', metavar='n', default=10, type=int, help='begin line number at n (default: 10)')
    group2.add_argument('-i', '--increment', metavar='n', default=10, type=int, help='set line number increments by n (default: 10)')
    group2.add_argument('-n', '--no-decl', action='store_true', required=False, help="no need to declare scalar variables with Dim before using them")
    group2.add_argument('-l', '--line-size', metavar='n', default=254, required=False, help="maximum line size (default: 254)")
    group2.add_argument('-k', '--tokenize', action='store_true', required=False, help="generate tokenized MSX-BASIC output")
    args = argp.parse_args(None if sys.argv[1:] else ['--help'])

    if args.version:
        term = shutil.get_terminal_size((80, 25))
        title = textwrap.fill('HitBasic version 0.4.0', width=term.columns)
        copyright = textwrap.fill('Copyright (c) 2020, Pedro Vaz de Mello de Medeiros', width=term.columns)
        disclaimer = textwrap.fill('''\
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.''',
                width=term.columns)

        print("%s\n\n%s\n\n%s\n" % (title, copyright, disclaimer))
        argp.exit(status=0)

    if args.x:
        source_code = """
                Screen 2,,1
' 1st variant
10 Let A$ = Val("Bla123" + "456")
12 B$ = Val("Bla123" + "456")
13 Goto @bla
Select a
Case 1
    Cls
    Print
Case 2
    'Play "A"
    Print
End Select

@bla Screen 2,,,,,1
Screen 2,,,,,1

Color 15,1,1

Line (0,0)-Step(100,100),4,bf
"""
        mm = hitbasic.create_metamodel(debug=True)
        model = create_model(mm, source_code, args.graphviz)
        print('==============')
        for stmt in model.statements:
            print(stmt.debug())
        print('-------------')
        generator = ascii_file.Generator()
        output = generator.process(model.statements)
        print(output.getvalue().decode('utf-8'))
        argp.exit(status=0)

    if args.stdin is True:
        args.c = [sys.stdin]
    if args.output is None:
        args.output = open('./output.asc', 'w')
    else:
        args.output = open(args.output, 'w')

    # Create text string from file or stdin and run it through the parser
    from hitbasic import hitbasic
    mm = hitbasic.create_metamodel(debug=args.graphviz)

    if args.stdin == True:
        sources = ''
        for file in args.c:
            sources += args.c[0].read()
        try:
            model = create_model(mm, sources, args.graphviz)
        except Exception as e:
            print('* %s error: %s' % (e.__class__.__name__, str(e)))
            if hasattr(args, 'debug') and args.debug:
                raise e
            argp.exit(status=-1)
    else:
        # TODO: and when there are multiple files?
        try:
            model = mm.model_from_file(args.c[0].name)
        except Exception as e:
            print('* %s error: %s' % (e.__class__.__name__, str(e)))
            if hasattr(args, 'debug') and args.debug:
                raise e
            argp.exit(status=-1)

    # Run output tree through the node visitor
    with open('./teste.out', 'w') as file:
        for statement in model.statements:
            print(statement, file=file)
