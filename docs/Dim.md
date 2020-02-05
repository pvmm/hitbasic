# Dim

In MSX-BASIC, the _DIM_ statement is used only to declare arrays and reserve memory space for them. In HitBasic it's used to declare any variable and its type, and optionally also sets a starting value.

```vb
Dim <variable>[<type symbol>][(<index>)] [As <type>] [= <value>]
```

Scope depends on where the variable is being declared. If declared in the main routine, its scope is global and therefore the variable can be known by every subroutine and function. Conversely, if the variable is declared inside a function or subroutine, its scope is local to that function or subroutine. And local scope always overrides global scope.

Type can be defined as either a suffixed symbol (like in MSX-BASIC) or by using the _As_ keyword, followed by the name of the type, but not both at the same time. The following table lists supported types, their suffixes, their value ranges and their memory footprint:

Type   |Suffix|Description                          |Value range                                     |Data footprint
-------|------|-------------------------------------|------------------------------------------------|-------------------------------------------------
Integer|%     |Integer                              |-32768 to 32767                                 |2 bytes
Single |!     |Floating point with single precision |6 significant digits, exponent from -64 to +62  |4 bytes
Double |#     |Floating point with double precision |14 significant digits, exponent from -64 to +62 |8 bytes
String |$     |String                               |0 to 255 characters                             |As many bytes as the number of characters, plus 3

If omitted, type is always floating point with double precision.
