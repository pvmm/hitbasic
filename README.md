# HitBASIC
PEG parser for MSX-BASIC on steroids

How to generate a new grammar
-----------------------------

`BASIC.py` contains the grammar transformed into code and it's generated from the rules contained in the file `BASIC.peg`. So if you change the rules, you should generate a new `BASIC.py` file. To generate this file you will need node.js and npm installed on your system. In the root directory execute the following commands:

```
$ npm install
$ ./scripts/generate-grammar.sh
```

Executing the parser
--------------------

The parser reads standard input and generate debug information for output (no transpilation yet). But you can at least use it to verify if the input is a valid HitBASIC program (the `docs` directory contains specifications of what constitutes a valid HitBASIC program).

```
$ python ./parser.py
for i 1 to 20
print i
next i
Parse error: line 1: expected [ \t], "="
for i 1 to 20
      ^
```
