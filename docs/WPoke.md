# WPoke

_WPoke_ is a new command that stores a 16-bit value directly into a memory address, and it has the following syntax:

```vb
WPoke <address>, <value>
```

Since a 16-bit value is made of two bytes, <address> receives the LSB (less significant byte) and <address> + 1 gets the MSB (most significant byte). Both <address> can be an expression valid in the range from -32768 to 65535. However, <value> should be an integer 16-bit value and will be valid in the range from -32768 to 32767. Negative numbers are in binary complement, which means -1 = &HFFFF. For example:

```vb
WPoke &HE000, &H1234
```

This writes &H12 at &HE000 and &H34 at &HE001. It could be transpiled as this:

```vb
POKE &HE000,&H34
POKE &HE001,&H12
```

But the above only works if we use values, not expressions. If you have expressions, then:

```vb
WPoke memPos, memVal
```

Assuming _memPos_ gets transpiled as _A_ and _memVal_ gets transpiled as _B_:

```vb
POKE (A),VAL("&H"+HEX$(B)) AND 255
IF (B)<0 THEN POKE (A)+1,VAL("&H"+LEFT$(HEX$(B),2)) ELSE POKE (A)+1,(B)\256
```

The parenthesis are to ensure the expressions are evaluated first.

## Warning

The MSX-BASIC _POKE_ instruction supports non-integer numbers as both the address and the value to be stored. We strongly advise against doing this as it can lead to unpredictable results or unexpected errors.
