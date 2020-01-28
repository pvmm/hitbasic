# WPoke

_WPoke_ is a new command that stores a 16-bit value directly into a memory address, and it has the following syntax:

```vb
WPoke <address>, <value>
```

Since a 16-bit value is made of two bytes, <address> receives the LSB (less significant byte) and <address> + 1 gets the MSB (most significant byte). Both address and value can be expressions and will be valid in the range from -32768 to 65535. Negative numbers are in binary complement, which means -1 = 65535. For example:
    
```vb
WPoke &HE000, &H1234
```

This writes &H12 at &HE000 and &H34 at &HE001. It could be transpiled as this:

```vb
Poke &HE000, &H34
Poke &HE001, &H12
```

But the above only works if we use values, not expressions. If you have expressions, then:

```vb
WPoke memPos, memVal
```

Assuming _memPos_ gets transpiled as _A_ and _memVal_ gets transpiled as _B_:

```vb
POKE (A), (B) MOD 256
IF B<0 THEN POKE (A)+1,(65536+B)\256 ELSE POKE (A)+1,(B)\256
```

The parenthesis are to ensure the expressions are evaluated first.