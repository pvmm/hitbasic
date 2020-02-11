# WPeek()

_WPeek_ is a new function that retrieves a 16-bit value directly from a memory address, and it has the following syntax:

```vb
WPeek(<address>)
```

Since it is a function, it returns a value that can be used in any expression or be attributed to a variable. For example:

```vb
memVal = WPeek(memPos)
```

The example above will return an integer value in the range from -32768 to 32767. Since a 16-bit value is made of two bytes, the LSB (less significant byte) is retrieved from <address> and the MSB (most significant byte) is retrieved from <address> + 1. Be aware that 16-bit integer values are always signed and negative numbers are in binary complement.

Considering _memVal_ gets transpiled as _A_ and _memPos_ as _B_, the previous snippet becomes this:

```vb
A=VAL("&H"+HEX$(PEEK(B)+PEEK((B)+1)*256))
```

The parenthesis are to ensure the expressions are evaluated first.

## Warning

The MSX-BASIC _PEEK()_ function supports non-integer numbers as the address. We strongly advise against doing this as it can lead to unpredictable results or unexpected errors.
