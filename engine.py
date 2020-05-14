import random

NUMS = "0123456789abcdef"

MATH_OP = {"+":"+",
           "-":"-",
           "*":"*",
           ",":"/",
           "%":"%"
          }

COMP_OP = { "(":"<",
            ")":">",
            "=":"=="
          }

ARROWS = {"<":(-1, 0), "^":(0,-1),
          ">":( 1, 0), "v":(0, 1)
         }
MIRRORS = { "/":  lambda x,y: (-y, -x),
            "\\": lambda x,y: (y, x),
            "|":  lambda x,y: (-x, y),
            "_":  lambda x,y: (x, -y),
            "R":  lambda x,y: (-x, -y)
          }


class Interpreter(object):
    def __init__(self, fileName):
        # IP variables
        self._x = -1 # Location in code
        self._y = 0
        self._direction = ARROWS[">"] 
        self._skip = False # Should the IP skip the next instruction?

        # code variables
        self._fileName = fileName
        self._width = 0  # Used for wrapping
        self._height = 0
        self._strMode = False
        self._code = self._getCode(fileName) 
        self._running = False
        self._currentStack = []
        self._savedStacks = [] # For when we want to create multiple of them
        self._register = [None] # Array for multiple stacks


    def _getCode(self, fileName):
        code = []
        self._height = 0
        self._width = 0

        with open(fileName, "r") as f:
            # Getting all of the code (Pass 1)
            for line in f: # go through all lines
                temp = []
                self._height += 1
                self._width = len(line) if self._width < len(line) else self._width

                if line.strip() == "//": break # After "//" all is comments

                for char in range(len(line) - 1): # go through all the characters in the line
                    temp.append(ord(line[char]))
                code.append(temp)

        # Make sure that that all lines are the same width (Pass 2)
        # This is to make sure that wrapping works
        for i in range(len(code)):
            while len(code[i]) != self._width:
                code[i].append(ord(" "))

        return code
    def _pop(self):
        return self._currentStack.pop()

    def _push(self, item):
        self._currentStack.append(item)

    def _move(self):
        # Move the IP
        self._x += self._direction[0]
        self._y += self._direction[1]

        # Wrap around
        if self._x >= self._width: self._x = 0
        if self._x < 0: self._x = self._width - 1

        if self._y >= self._height: self._y = 0
        if self._y < 0: self._y = self._height - 1

        if self._skip:
            self._skip = False
            self._move()

    def _interpret(self, currInst):
        # Movement
        if currInst in ARROWS:
            # Normal arrows
            self._direction = ARROWS[currInst]

        elif currInst in MIRRORS:
            # Mirrors
            self._direction = MIRRORS[currInst](self._x, self._y)

        elif currInst == "?":
            # Random Direction
            self._direction = ARROWS[random.choice(list(ARROWS))]

        elif currInst == "#":
            # Trampoline
            self._skip = True

        elif currInst == "j":
            # Jump to a point
            self._y, self._x = self._pop(), self._pop()
        
        # Operators - Normal
        elif currInst in NUMS:
            # Push constants
            self._push(int(currInst, len(NUMS)))

        elif currInst in MATH_OP:
            # Perform Math (+, -, *, /, %)
            y, x = self._pop(), self._pop()
            self._push(eval("{} {} {}".format(str(x), MATH_OP[currInst], str(y))))

        elif currInst == "&":
            # Put something in the current register...
            currentReg = self._register.pop()
            if currentReg == None:
                self._register.append(self._pop())
            else:
            # ...or take something out.
                self._push(currentReg)
                self._register.append(None)

        # If statments
        elif currInst == "`":
            # Skippy
            self._skip = True if self._pop() == 0 else False

        elif currInst == "I":
            # Vertial
            self._direction = ARROWS["v"] if self._pop() == 0 else ARROWS["^"]

        elif currInst == "i":
            # Horizontal
            self._direction = ARROWS[">"] if self._pop() == 0 else ARROWS["<"]


        # Stack Operators
        elif currInst == "r":
            # Reverse the stack
            self._currentStack = self._currentStack[::-1]

        elif currInst == "[":
            # Create a new stack and register
            x = self._pop()
            self._savedStacks.append(self._currentStack[:len(self._currentStack) - x])
            self._currentStack = self._currentStack[x - 1:]
            self._register.append(None)

        elif currInst == "]":
            # Takes the current stack and adds it to the one below
            # Also, it gets rid of the register.
            self._register.pop()
            self._currentStack = self._savedStacks.pop() + self._currentStack

        elif currInst == "{":
            # Shift the stack left
            self._currentStack.insert(len(self._currentStack) - 1, self._currentStack.pop(0))

        elif currInst == "}":
            # Shift the stack right
            self._currentStack.insert(0, self._currentStack.pop())

        elif currInst == "~":
            # Discard the top value
            self._pop()

        elif currInst == ":":
            # Duplicate the top of the stack, put 0 if there is nothing
            if len(self._currentStack) == 0:
                self._currentStack.append(0)
            else:
                self._currentStack.append(self._currentStack[len(self._currentStack) - 1])

        elif currInst == "s":
            # Swap the last two elements pushed onto the stack
            x, y = self._pop(), self._pop()
            self._push(x)
            self._push(y)

        elif currInst == "l":
            self._push(len(self._currentStack))

        # Operators - Comparison
        elif currInst in COMP_OP:
            y, x = self._pop(), self._pop()
            if eval("{} {} {}".format(x, COMP_OP[currInst], y)):
                self._push(1)
            else:
                self._push(0)

        elif currInst == "!":
            if self._pop() == 0:
                self._push(1)
            else:
                self._push(0)

        elif currInst == "\"":
            self._strMode = not self._strMode

        elif currInst == "o":
            # Output as an ASCII character (TODO)
            pass

        elif currInst == "n":
            # Output as a decimal number (TODO)
            pass

        elif currInst == "h":
            # Output as a hex number (TODO)
            pass
        
        elif currInst == "p":
            # Put z at (x, y)
            y, x, z = self._pop(), self._pop(), self._pop()
            self._code[y][x] = z

        elif currInst == "g":
            # Get a value from the code
            y, x = self._pop(), self._pop()
            self._push(self._code[y][x])

        elif currInst == " ":
            # Nop
            pass

        elif currInst == ";":
            # End execution
            self._running = False

        else:
            self._running = False
            print("Eh?! I don't know what is this: " + currInst)

        print("currInst: ", currInst,", Register:  ", self._register, ", stack: ", self._currentStack)

    def _run(self):
        # Initalize
        self._currentStack = []
        self._savedStacks = []
        self._register = [None]
        self._running = True

        while self._running:
            currentInst = " "
            while currentInst == " ": # Skip over spaces
                self._move()
                currentInst = chr(self._code[self._y][self._x])
            self._interpret(currentInst)
            
        


