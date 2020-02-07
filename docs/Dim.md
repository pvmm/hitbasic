# Dim

In MSX-BASIC, the _DIM_ statement is used only to declare arrays and reserve memory space for them. In HitBasic it's also used to declare any variable and its type, and optionally also sets a starting value.

Its basic form is as follows:

```vb
Dim <variable> [, <variable> ...]
```

This means you can declare more than one variable with a single _Dim_ statement. Each variable has the following syntax and parts:

```
name[<type suffix>] [([<bounds list>])] [As <type>] = <value>
```

## Scope and name

Scope depends on where the variable is being declared. If declared in the main routine, its scope is global and therefore the variable can be known by every subroutine and function. Conversely, if the variable is declared inside a function or subroutine, its scope is local to that function or subroutine. And local scope always overrides global scope. HitBasic, unlike MSX-BASIC, support variable names with any number of characters. The only restriction is that the variable name must not be a reserved keyword.

## Type

Type can be defined as either a suffixed symbol (like in MSX-BASIC) or by using the _As_ keyword, followed by the name of the type, but not both at the same time. The following table lists supported types, their suffixes, their value ranges and their memory footprint:

Type   |Suffix|Description                          |Value range                                     |Data footprint
-------|------|-------------------------------------|------------------------------------------------|-------------------------------------------------
Integer|%     |Integer                              |-32768 to 32767                                 |2 bytes
Single |!     |Floating point with single precision |6 significant digits, exponent from -64 to +62  |4 bytes
Double |#     |Floating point with double precision |14 significant digits, exponent from -64 to +62 |8 bytes
String |$     |String                               |0 to 255 characters                             |As many bytes as the number of characters, plus 3
Boolean|      |Can store only two logic states      |_False_ or _True_                               |2 bytes (it's stored as an integer)

If omitted, type is always floating point with double precision, unless defined otherwise (see keywords _DefInt_, _DefSng_, _DefDbl_, _DefStr_ and _DefBool_). _Boolean_ is a new type to HitBasic which can only hold values _False_ or _True_. These are internally converted to integer.

For example, to declare _n_ as a floating point variable with single precision:

```vb
Dim n As Single
```

Declaring multiple variables with one _Dim_ keyword:

```vb
Dim address As String, zipCode As Double
```

Declaring multiple variables with starting values:

```vb
Dim year As Integer = 2020, pi As Single = 3.14159
```

If you try to assign a starting value without an explicit type, HitBasic will use type inference to determine the type instead of just using the default. For example:

```vb
Dim name = "John"
```

In the previous case, the variable is considered as a string. In the case of numeric values, type will always be the smaller type that can hold the value. Like this:

```vb
Dim year = 2020 ' The type is _Integer_ because the value is an integer in the range from -32768 to 32767
Dim tau = 6.28319 ' The type is _Single_ because the value is floating point and it has 6 or less significant digits
Dim pi = 3.1415926535898 ' The type is _Double_ because the value is floating point
```

Declaring multiple variables of the same type:

```vb
Dim name, surname As String
```

Declaring multiple variables with multiple types:

```vb
Dim name, surname, address As String, year, month, day As Integer
```

In both previous cases, since multiple variables are being defined with a single type, it isn't possible to assign a starting value to the variables.

## Arrays

If you follow the variable name with parentheses, it means you are declaring an array. Arrays can have up to 3 dimensions. The bounds list is composed by each dimension's bounds, separated by commas (,), like this:

```vb
Dim a(1 To 20, 1 To 10) As Double
```

The previous snippet declared a two-dimensional array named _a_ with indexes varying from 1 to 20 in the first dimension and from 1 to 10 in the second dimension, and double precision floating point elements.

When declaring an array, the lower bound can be omitted; in this case, it's considered to be zero. So `Dim a(9)` is the same as `Dim a(0 To 9)`. If both lower and upper bounds are omitted, they are considered to be zero and 10, respectively. So `Dim b()` is the same as `Dim b(0 To 10)`. 

Just like with other variables, you can set a starting value for an array, by using an array literal:

```vb
Dim primes() As Integer = {2, 3, 5, 7, 11, 13, 17}
```

In the case above, no bounds were specified, but since there are 7 elements in the array literal, this is considered to be an array with 7 elements (from 0 to 6). This also works for multidimensional arrays:

```vb
Dim a(1 To 3, 0 To 1) As Integer = {{1, 2, 3}, {2, 3, 4}, {3, 4, 5}, {4, 5, 6}}
```
