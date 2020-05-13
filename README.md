# Befish

It's like Befunge-93 and ><> combined

## Movement
^<>v    IP redirection (up, left, right and down)

/\      Mirrors
_|

R       Reflect no matter what

?      Sends the IP in random direction

;      Ends execution

\#      Jump over the next instruction

j     Pop y then x then jump to (x, y) keeping the current direction.
       Moves for one tick before starting execution like normal

## Operators
### Normal

0-9   Constants you can push onto the stack in hexadecimal
a-f

\+ -  Plus, minus, multiply and divide. Pops y then x, then,
\* ,  performs x (operator) y and pushes the result onto the stack

%    Pops y then x then pushes x mod y

&    Pops one value then stores it in the register. Use it again to
     retrieve it. (one per stack)

`   Pop a value, if it's 0 then jump over the next instruction
    (backtick)

I   Pop a value, if it's 0, the IP goes down else it goes up

i   Pop a value, if it's 0, the IP goes right else it goes left

## Stack operators

r   reverse the current stack

x[  Pops x then takes the previous x items into another stack

]   Puts the current stack onto the one below it

{}  Shift the stack left and right respectively

\~  Discard the top value of the stack

\:  Duplicate the top value of the stack

s  Swap the top two values of the stack

l  Push the length of the stack onto the stack

## Comparison operators

(   Pops y then x then does x < y. If true, it pushes 1 else
    0

)   Pops y then x then does x > y. If true, it pushes 1 else
    0

=  Pops y then x then does x == y. If true, it pushes 1 else
   0

!  Pops a value, if it's a 0, it pushes a 1 else a 0

## I/O

"  Toggle string mode. Everything after it will be considered as a character not a command until the next double quote.

o  Pop one value then output it as a character

n  Pop one value then output it as a number

h  Pop one value then output it as a hex number

p  Pop y then x then z. It stores z at (x, y)

g  Pop y then x. It pushes the value stored at (x, y). If there
   is nothing there it pushes 10

