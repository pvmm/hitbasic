# Function

_Function_ is used to define functions and parameters to be passed. A function is a subroutine that returns with one or more values. The structure looks like this:

```vb
Function <name>[(<parameter 1> [As <type 1>]{[, <parameter 2...>] [As <type 2...>]})] [As <type> | As (list of types)]
	...
	[Return [<value 1>{[, <value 2>]}]
	...
	[Exit Function]
	...
End Sub
```

You can have as many parameters as you want, each one separated by a comma (","). Each parameter can optionally have its type specified. For example:

```vb
Input year
If isLeapYear(year) Then
	Print year; " is a leap year"
Else
	Print year; " is NOT a leap year"
End If
End

Function isLeapYear(myYear As Integer) As Boolean
	Return (year Mod 4) = 0
End Function
```

In the case above, in order for the function to return a value, it gets its own symbol, just like variables and parameters:

```vb
INPUT A
B=A:GOSUB @isLeapYearStart
IF C THEN PRINT A; " is a leap year" ELSE PRINT A; " is NOT a leap year"
END

@isLeapYearStart
C=(B MOD 4)=0
RETURN
```

Just like with _Sub_, function parameters are not the same as variables when they share the same name. Beware when using parameters with the same name as previously declared variables, as it may lead to unintended behavior.

## Tuples

As seen above, a function can return more than one value. These are called _tuples_. In this case, _As_ should refer to a list of types (inside parentheses), instead of only one type. For example:

```vb
Input date
day, month, year = stringToDate(date)
Print "Today is "; strMonth(month - 1); day; " of"; year
End

Function stringToDate(myDate As String) As (Integer, Integer, Integer) 
    Dim myDay, myMonth, myYear As Integer
    myDay = Val(Left(myDate, 2))
    myMonth = Val(Mid(myDate, 3, 2))
    myYear = Val(Right(myDate, 4))
    Return myDay, myMonth, myYear
End Function
```

The above would be transpiled as something like this:

```vb
Input A$
B$=A$:GOSUB @stringToDate
F%=C%:G%=D%:H%=E%
PRINT "Today is "; C$(G%-1);F%;" of";H%
END

@stringToDate
C%=VAL(LEFT$(B$,2))
D%=VAL(MID$(B$,3,2))
E%=VAL(RIGHT$(B$,4))
RETURN
```

In the previous example, _date_ became _A$_, while _day_, _month_ and _year_ became, respectively, _F%_, _G%_ and _H%_. The function _stringToDate()_ had its parameters and values (_myDate_, _myDay_, _myMonth_, _myYear_) transpiled into _B$_, _C%_, _D%_ and _E%_.


## Keyword _Exit Function_

The _Exit Function_ keyword is used to leave a subroutine block and should be transpiled as `RETURN`. However, you should assign a value to the function to prevent unexpected behavior. For example:

```vb
Function wordYear(lang As String) As String
	If lang = "PT" Then
		wordYear = "ano"
		Exit Function
	End If
	wordYear = "year"
End Function
```

The snippet above is functionally equivalent to this one:

```vb
Function wordYear(lang As String) As String
	If lang = "PT" Then
		Return "ano"
	End If
	Return "year"
End Function
```

The two previous snippets would both become something like this, if _wordYear_ is transpiled to _A$_ and _lang_ to _B$_:

```vb
@wordYearStart
IF B$="PT" THEN A$="ano":RETURN
A$="ano"
RETURN
```

It comes to the programmer's preference which form to use. We recommend to always go for clarity, so we favor the _Return <value>_ form.

## Keyword _Return_

As seen above, _Return_ is used to assign one or more values for a function to return. If used without any parameters, it is equivalent to _Exit Function_, so be careful. Since in MSX-BASIC _RETURN_ accepts a line number as a parameter, you can also use it the same way in HitBasic. Just use a label as a parameter. Of course, this sacrifices code readability and should be avoided.
