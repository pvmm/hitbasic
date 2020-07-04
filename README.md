# HitBasic
High level BASIC dialect emulates Visual Basic features transpiled to MSX-BASIC

How to execute HitBasic
-----------------------

Install Python 3.8.x and pip, the package installer for Python, then execute the following command:

```
$ pip install -r requirements.txt
```

Usage
-----

Executing **HitBasic** without parameters returns the following help message:

```
$ ./hb
usage: hb [-h] (-t | --version | -c .ASC infile [.ASC infile ...] | -s) [-o outfile] [-v] [-b n] [-i n] [-n] [-l n] [-k] [-e]

HitBasic transpiles high level Visual Basic like language into MSX-BASIC.

optional arguments:
  -h, --help            show this help message and exit
  -t, --tests           run collection of tests
  --version             display version and finishes
  -c .ASC infile [.ASC infile ...]
                        compile source from infile(s)
  -s, --stdin           transpile to MSX-BASIC program from standard input

override default configuration:
  -o outfile, --output outfile
                        write into outfile (default: out.asc)
  -v, --short-vars      force BASIC short length variables mode
  -b n, --begin n       begin line number at n (default: 10)
  -i n, --increment n   set line number increments by n (default: 10)
  -n, --no-dim          no need to declare non-arrays with Dim before using them
  -l n, --line-size n   maximum line size (default: 254)
  -k, --tokenize        generate tokenized MSX-BASIC output
  -e, --clean           generate clean and readable source code

For bug report, suggestions, praises or complains, please go to: <https://github.com/pvmm/hitbasic>.

$ █ 
```

The transpiler reads standard input with the `-s` parameter or it can read `.ASC` (ASCII source code) files with the `-c` parameter and generate code in "pretty-print" format and debug information with the `-d` parameter.


```
$ ./hb -s
for i 1 to 20
print i
next i
* NoMatch error: Expected '(' or '=' at position (1, 7) => 'for i *1 to 20 pr'.
```

The `docs` directory contains specifications of what constitutes a valid **HitBasic** program.
