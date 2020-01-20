# Do Loop

This is the _Do Loop_ structure. It works like this:

```vb
Do [While <condition>]|[Until <condition>]
	...
Loop [While <condition>]|[Until <condition>]
```

Conditions can be tested at the beginning of the loop (before the loop runs once) and at the end of the loop (after the loop runs at least once). The _While_ keyword tests for a condition that tests true, and the _Until_ keyword tests for a condition that tests false. The following table makes it more clear:

Condition test           | Consequence
------------------------ | --------------------------------------------------------------------------------------------
`Do While <condition>`   | If <condition> tests true, executes the loop. If false, jumps to the end of the loop.
`Do Until <condition>`   | If <condition> tests false, executes the loop. If true, jumps to the end of the loop.
`Loop While <condition>` | If <condition> tests true, jumps back to the beginning of the loop. If false, ends the loop.
`Loop Until <condition>` | If <condition> tests false, jumps back to the beginning of the loop. If true, ends the loop.

If no conditions are tested, the loop runs indefinitely. For example:

```vb
Do
	...
Loop
```

This becomes:

```vb
@DoLoopStart
	...
GOTO @DoLoopStart
@DoLoopEnd
```

## _Do While_

```vb
Do While <condition>
	...
Loop
```

Becomes:

```vb
@DoLoopStart
IF NOT(<condition>) THEN @DoLoopEnd
	...
GOTO @DoLoopStart
@DoLoopEnd
```

## Do Until

```vb
Do Until <condition>
	...
Loop
```

Becomes:

```vb
@DoLoopStart
IF <condition> THEN @DoLoopEnd
	...
GOTO @DoLoopStart
@DoLoopEnd
```

## Loop While

```vb
Do
	...
Loop While <condition>
```

Becomes:

```vb
@DoLoopStart
	...
IF <condition> THEN @DoLoopStart
@DoLoopEnd
```

## Loop Until

```vb
Do
	...
Loop Until <condition>
```

Becomes:

```vb
@DoLoopStart
	...
IF NOT(<condition>) THEN @DoLoopStart
@DoLoopEnd
```
## Keyword _Exit Do_

The _Exit Do_ keyword is used to break out of a _Do Loop_ block and should be transpiled as `GOTO @DoLoopEnd`. In fact, it's the only way to exit a _Do Loop_ block without any condition tests.
