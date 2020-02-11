# Sub

_Sub_ is used to define subroutines and parameters to be passed. The structure looks like this:

```vb
Sub <name>[(<parameter 1> [As <type 1>]{[, <parameter 2...>] [As <type 2...>]})]
	...
	[Exit Sub]
	...
End Sub
```

You can have as many parameters as you want, each one separated by a comma (","). Each parameter can optionally have its type specified. For example:

```vb
Sub printBeep(text As String)
	Print text
	Beep
End Sub
```

In the case above, if _text_ is transpiled to _A_, we have the following:

```vb
@printBeepStart
PRINT A$
BEEP
RETURN
```

Be aware that parameters are known only inside the subroutine, so when transpiled they get their own symbols. So be careful if you use parameters with the same name of variables in your program. For example:

```vb
text = "Test"
printBeep(text)
End

Sub printBeep(text As String)
	Print text
	Beep
End Sub
```

This may become:

```vb
A$="Test"
B$=A$:GOSUB @printBeepStart
END

@printBeepStart
PRINT B$	
RETURN
```

This happens because when evaluating symbols for the variables, the **variable** _text_ gets renamed to _A_, while the **parameter** _text_ in the subroutine _printBeep()_ gets renamed to _B_, and _B_ is used to get the parameters before the subroutine call. Indeed, if we call the subroutine directly:

```vb
printBeep("Test")
End

Sub printBeep(text As String)
	PRINT text
	BEEP
End Sub
```

Since we only have the parameter _text_, but not the variable, it gets renamed to _A$_. Thus:

```vb
A$="Test":GOSUB @printBeepStart
END

@printBeepStart
PRINT A$
BEEP
RETURN
```

## Keyword _Exit Sub_

The _Exit Sub_ keyword is used to leave a subroutine block and should be transpiled as `RETURN`.

## Keyword _Return_

It should be mentioned that subroutines in MSX-BASIC end with the keyword _RETURN_, which transfers control to the following instruction after the _GOSUB_ that called the subroutine, unless a line number is specified. In HitBasic, _Return_ is simply equivalent to _Exit Sub_, but it's possible to use a label as a parameter, in order to leave a subroutine and return to a specific line. This sacrifices code readability and should be avoided. For example:

```vb
Return @mainLoop
```
