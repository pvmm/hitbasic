# Supported Keywords

These keywords are recognized by HitBasic and are mostly compatible with MSX-BASIC keywords, unless noted.

## Conditional Execution

Keyword        | Remarks
---------------|--------------------------------------------------------------------------------------------
`End Select`   | New to HitBasic
`End If`       | New to HitBasic
`If GoTo Else` | It's recommended to use `If Then Else` instead
`If Then Else` | In HitBasic, this structure can be multiline, using the keyword `End If` to close the block
`On GoSub`     |
`On GoTo`      |
`Select Case`  | New to HitBasic

## Clock and Timing

Keyword                  | Remarks
-------------------------|--------
`Call Pause` or `_Pause` | tR
`Interval`               |
`Get Date`               | MSX2
`Get Time`               | MSX2
`On Interval Gosub`      |
`Set Date`               | MSX2
`Set Time`               | MSX2
`Time`                   |

## Data Conversion Functions

Keyword             | Remarks
--------------------|------------------------------------------
`Asc()`             |
`Bin()` or `Bin$()` | In HitBasic, the trailing _$_ is optional
`CDbl()`            |
`Chr()` or `Chr$()` | In HitBasic, the trailing _$_ is optional
`CInt()`            |
`CSng()`            |
`Hex()` or `Hex$()` | In HitBasic, the trailing _$_ is optional
`Oct()` or `Oct$()` | In HitBasic, the trailing _$_ is optional
`Str()` or `Str$()` | In HitBasic, the trailing _$_ is optional
`Val()`             |

## Flow Control

Keyword    | Remarks
-----------|--------------------------------------------------------
`For Next` |
`GoSub`    |
`GoTo`     |
`Return`   |

## Operators

### Arithmetic Operators

Operator | Meaning                      | Precedence
---------|------------------------------|-----------
`^`      | Exponentiation               | 13
`-`      | Negation                     | 12
`*`, `/` | Multiplication and Division  | 11
`\`      | Integer Division             | 10
`Mod`    | Modulus (Division Remainder) | 9
`+`, `-` | Addition and Subtraction     | 8

For all purposes and effects, `+` as a string concatenation operator has the same precedence as itself as an arithmetic operator.

### Comparison Operators

All comparison operators (`=`, `<>`, `<`, `<=`, `>`, `>=` and `Is`) have the same precedence, which is 7, hence all arithmetic operations are evaluated before comparisons.

### Logical and Bitwise Operators

Operator | Meaning                      | Precedence
---------|------------------------------|-----------
`Not`    | Negation                     | 6
`And`    | Conjunction                  | 5
`Or`     | Inclusive Disjunction        | 4
`Xor`    | Exclusive Disjunction        | 3
`Eqv`    | Logical Equivalence          | 2
`Imp`    | Logical Implication          | 1
