# If Then Else

This is the _If Then Else_ structure. It tests for a condition and if the condition tests true, does something. Optionally, it can do something if the condition tests false. Alternatively, it can also be used to jump to a specific line. In MSX-BASIC, the entire structure must be on a single program line, but in HitBasic the structure can have multiple lines, organized in blocks, like other structured languages.

## Single-line

It looks like this:

```vb
If <condition> Then <action> [Else <else-action>]
```

Just like in MSX-BASIC, the actions can be a single statement, a sequence of statements separated by a colon (:) or a label (in this case, it's equivalent to a line number). If it's a label, it's equivalent to `GoTo <label>`. There's also a variation that, in MSX-BASIC, only supports line numbers, and in HitBasic, labels:

```vb
If <condition> GoTo <label> [Else <else-label>]
```

If you must use conditional jumps in your program, this is the preferred form because of slightly superior performance.

## Multiline

The multiline syntax requires that each clause must be the only statement in the line, optionally preceded by a label. Also, the keyword `Then` becomes optional, but it's recommended for clarity's sake. Finally, the end of the block must be indicated with `End If`. Like this:

```vb
If <condition> [Then]
	[<action>]
[Else
	[<else-action>]]
End If
```

For example:

```vb
If age >= 18 Then
	Print "This person is an adult."
Else
	Print "This person is a minor."
End If
```

Assuming _age_ becomes _A_, this becomes:

```vb
IF A>=18 THEN GOSUB @IfThen ELSE GOSUB @IfElse
END

@IfThen:
PRINT "This person is an adult."
RETURN

@IfElse:
PRINT "This person is a minor."
RETURN
```

The blocks get separated in subroutines since this is the only way they can support multiple statements without exceeding maximum line size. If you need, you can nest structures, like this:

```vb
If age >= 18 Then
	Print "This person is an adult."
Else
	Print "This person is a minor."
	If age >= 16 Then
		Print "And this person can vote."
	Else
		Print "And this person can't vote."
	End If
End If
```

Which, assuming _age_ gets transpiled as _A_, becomes something like this:

```vb
IF A>=18 THEN GOSUB @IfThen1 ELSE GOSUB @IfElse1
END

@IfThen1:
PRINT "This person is an adult."
RETURN

@IfElse1:
PRINT "This person is a minor."
IF A>=16 THEN GOSUB @IfThen2 ELSE GOSUB @IfElse2
RETURN

@IfThen2:
PRINT "And this person can vote."
RETURN

@IfElse2:
PRINT "And this person can't vote"
```

Just be careful when nesting these structures, because each instance will require more memory.
