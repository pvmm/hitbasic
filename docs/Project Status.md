Project Status
==============

This document reflects the status of the HitBasic transpiler.  It is a live document and will be updated as work progresses and new features are planned.  This is not an exhaustive list of our features but rather the ones which have active development efforts behind them.


| Language Feature   | Grammar% | Parser% |
| ------------------ | -------- | ------- |
| Dim clauses            | 80%  | 30% |
| If clauses             | 100% | 0%  |
| Select clauses         | 100% | 60% |
| Do Loops               | 100% | 80% |
| For Loops              | 80%  | 70% |
| Print instruction      | 100% | 70% |
| Functions              | 70%  | 0%  |
| Subroutines            | 0%   | 0%  |
| Subroutine/function calls | 100%  | 30% |
| Boolean type           | 0%   | 0%  |
| Legacy maths/logic expressions | 100% | 60% |
| Def Fn functions       | 0%   | 0%  |
| Remaining instruction set | 1%   | 0%  |

| Software components & features   | Status |
| -------------------------------- | ------ |
| Preprocessor (*)       | 70% |
| Scope management       | 30% |
| MSX-BASIC translation  | 30% |
| MSX-BASIC tokenizer    | 0%  |
| Symbol table           | 40% |
| Errors and warnings reporting | 10% |
| Boolean type support   | 0%   |
| Python unit testing    | 100% |
| test functions         | 30% |

(*) For PEG parsers, a preprocessor was not really necessary, but it has proven useful for making the grammar simpler to read and maintain. It also makes parser error reports more meaningful for the user.

