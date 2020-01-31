# For Next

This is the _For Next_ structure. It uses a counter variabe to count from one number to another, incrementing the counter by 1 and executing everything inside the loop each iteration. It optionally increments the counter by any other arbitrary value:

```vb
For <counter> = <start> To <end> [Step <step>]
	...
Next <counter>
```

Please note: in MSX-BASIC the _Next_ doesn't require a variable, but for clarity and good practice's sake the variable is mandatory in HitBasic. In the final MSX-BASIC it will be omitted, though. For example:

```vb
For counter = 1 To 10
	Print counter
Next counter
```

Assuming _counter_ gets transpiled as _A_:

```vb
@ForStart
FOR A=1 TO 10
	PRINT A
@ForEnd
NEXT
```

## Keyword _Continue For_

_Continue For_ just transfer control to the next loop iteration. For example:

```vb
For counter = 1 To 10
	If (counter Mod 2) = 0 Then
		Continue For
	End If
	Print counter
Next counter
```

In the snippet above, when _counter_ is even the `Print counter` line isn't executed. Assuming _counter_ becomes _A_, it could be transpiled like this:

```vb
@ForStart
FOR A=1 TO 10
	IF (A MOD 2)=0 THEN GOTO @ForEnd
	PRINT A
@ForEnd
NEXT
```

## Keyword _Exit For_

_Exit For_ just breaks out of the _For Next_ structure and continues executing after the loop's end. For example:

```vb
For counter = 1 To 1000
	If Inkey = Chr(13) Then
		Exit For
	End If
Next counter
Print "Interrompido em "; counter
```

Assuming _counter_ is transpiled as _A_, this becomes:

```vb
GOSUB @ForStart
PRINT "Interrompido em "; A
END

@ForStart
FOR A=1 TO 1000
	IF INKEY$=CHR$(13) THEN RETURN
@ForEnd
NEXT
RETURN
```

The loop is moved to a subroutine because in MSX-BASIC, _RETURN_ empties the stack. If we just _GOTO_ed outside the _FOR_ loop, the counter variable would remain in the stack and an error would eventually be caused.