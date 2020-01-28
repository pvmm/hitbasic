# Select Case

This is the _Select Case_ structure. It works like this:

```vb
Select <testexpression>
Case <expressionlist>
    ...
Case Else
    ...
End Select
```

For example:

```vb
Select num
Case 1
    ...
Case 2
    ...
Case Else
    ...
End Select
```

If we assume the variable _num_ gets transpiled to _A_, we have:

```vb
@SelectStart
IF NOT(A=1) THEN @SelectCase2
	...
@SelectCase2
IF NOT(A=2) THEN @SelectCaseElse
	...
@SelectCaseElse
	...
@SelectEnd
```

If there is no _Case Else_ clause, the last condition test goes to @SelectEnd.

## Expression lists

Conditions can be tested against an expression list. For example:

```vb
Select num
Case 1, 3
    ...
Case 2
    ...
End Select
```

Assuming _num_ gets transpiled to _A_:

```vb
@SelectStart
IF NOT(A=1 OR A=3) THEN @SelectCase2
	...
@SelectCase2
IF NOT(A=2) THEN @SelectEnd
	...
@SelectEnd
```

## Keyword _Is_

The keyword _Is_ represents the test expression inside the expression list, and can be used with any comparison operator (=, <>, <, <=, > or >=). For example:

```vb
Select num
Case Is > min
	Print "It's larger"
Case Is < min
	Print "It's smaller"
Case Else
	Print "It's the same"
End Select
```

Assuming _num_ gets transpiled to _A_ and _min_ gets transpiled to _B_:

```vb
@SelectStart
IF NOT(A>B) THEN @SelectCase2
	PRINT "It's larger"
@SelectCase2
IF NOT(A<B) THEN @SelectCaseElse
	PRINT "It's smaller"
@SelectCaseElse
	PRINT "It's the same"
@SelectEnd
```

## Keyword _To_

The keyword _To_ is used to represent an interval inside the expression list:

```vb
Select num
Case 1 To 5
    Print "From 1 to 5"
Case 6 To 10
    Print "From 6 to 10"
End Select
```

So the conditions above should be transpiled as this:

```vb
@SelectStart
IF NOT(A>=1 AND A<=5) THEN @SelectCase2
	PRINT "From 1 to 5"
@SelectCase2
IF NOT(A>=6 AND A<=10) THEN @SelectEnd
	PRINT "From 6 to 10"
@SelectEnd
```

## Keyword _Exit Select_

The _Exit Select_ keyword is used to break out of a _Select Case_ block and should be transpiled as `GOTO @SelectEnd`.
