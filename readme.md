# CPU
This is a CPU emulator built in python. A thing to note is that all data storage mechanisms simulated by lists and dictionaries are accessed through the assembly language starting at 1, not zero.


## Registers
There are registers, numbered 1-16 where their values may be set, copied from RAM, copied to RAM, unset, and manipulated in other ways.

## Ram
The Random Access Memory is a dictionary with keys 1-32 where each key's value is a 32-value long array. It is the same for the screen

## Assembly
If you wish to code directly in assembly (suggested, as BASIC is not finished yet)
### Syntax
### Commands Where <code>a</code>, <code>b</code>, and <code>c</code> Are Registers:
For registers:
<code>CMD {a} {b} {c}</code><br>
(unreferenced letters SHOULD NOT be included in the command, ex <code>REM 1</code>(clears register 1, no other things listed))
|Command    |Description/Representation in Pseudocode    |
|--         |--             |
|__Arithmetic__|Math Operations|
|ADD        |c = a + b      |
|SUB        |c = a - b      |
|MUL        |c = a * b      |
|DIV        |c = a / b      |
|MOD        |c = a % b (modulus)|
|__Bitwise__|Operations on binary|
|AND        |c = a & b      |
|OR         |c = a \| b     |
|NOT        |b = !a         |
|__Registers__|Setting values, etc.|
|SET        |a = b (one exception, b is a number, not a register)|
|REM        |a = 0          |
|MOV        |b = a, a = 0 (moving value in a to b)|

### Commands Where <code>y</code> and <code>x</code> Are *x* and *y* Values of RAM Locations, and <code>c</code> is a Register
For RAM:
<code>CMD {y} {x} {c}</code><br>
(unreferenced letters SHOULD NOT be included in the command, ex <code>DEL 1 1</code>(clears value in the first RAM cell))<br>
<code>RAM(y,x)</code> Represents "*Ram value at x:<code>x</code> and y:<code>y</code>*".
|Command    |Description/Representation in Pseudocode    |
|--         |--             |
|LOAD       |c = RAM(y,x)   |
|SAVE       |RAM(y,x) = c   |
|DEL        |RAM(y,x) = 0   |

### Commands Where <code>y</code> and <code>x</code> Are *x* and *y* Values of Screen Locations, and <code>c</code> is a Register (Screen is set up exactly the same as RAM)
|Command        |Description/Representation in Pseudocode    |
|--             |--             |
|SCRNLOAD       |c = SCRN(y,x)   |
|SCRNSAVE       |SCRN(y,x) = c   |
|SCRNDEL        |SCRN(y,x) = 0   |
|SCRNSHOW       |Updates the screen|
|SCRNCLR        |Clears the entire creen|

### Control Flow
|Command        |Description    |
|--             |--             |
|HLT            |Halts all computation|