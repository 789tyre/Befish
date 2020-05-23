import curses
from curses import wrapper
from engine import *

class debugInterpreter(Interpreter):
    def __init__(self, fileName, waitTime=0.25):
        super().__init__(fileName)
        self._output = []
        self._stdscr = None
        self._waitTime = waitTime
        self._stdscrDimentions = None
        self._cursorLocation = [0, 0]

        self._Vpadding = 3

    def _input(self):
        self._cursorLocation = [self._height + self._Vpadding, 0] # Info starts one line down
        curses.echo()
        curses.curs_set(True)
        self._stdscr.addstr(*self._cursorLocation, "Enter input: ")
        temp = self._stdscr.getstr()
        for char in temp[::-1]:
            self._push(char)

        curses.noecho()
        curses.curs_set(False)
       

    def _charOutput(self):
        self._output.append(chr(self._pop()))

    def _numOutput(self):
        self._output.append(str(self._pop()))

    def _hexOutput(self):
        self._pop()

    def _init(self):
        self._currentStack = []
        self._savedStacks = []
        self._register = [None]
        self._running = True

        # Initializing Curses
        self._stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(False)
        self._stdscr.keypad(True)
        self._stdscrDimentions = self._stdscr.getmaxyx()

    def _wrappedRun(self):
        while self._running:
            # Step through the code
            self._move()
            currentInst = chr(self._code[self._IPy][self._IPx])
            self._interpret(currentInst)

            # Draw code
            self._cursorLocation = [0, 0]
            self._stdscr.clear()
            self._stdscr.move(*self._cursorLocation)
            for line in range(len(self._code)):
                for char in range(len(self._code[line])):
                    if line == self._IPy and char == self._IPx:
                        self._stdscr.addstr(*self._cursorLocation, chr(self._code[line][char]), curses.A_REVERSE)
                    else:
                        self._stdscr.addstr(*self._cursorLocation, chr(self._code[line][char]))

                    self._cursorLocation[1] += 1

                self._cursorLocation[0] += 1
                self._cursorLocation[1] = 0

            # Draw info
            self._cursorLocation[0] += self._Vpadding
            self._stdscr.addstr(*self._cursorLocation, """
Instruction: {}
Stack: {}
Register: {}
Output: {}""".format(
                    currentInst,
                    str(self._currentStack),
                    str(self._register),
                    "".join(self._output)
                ))

            self._stdscr.refresh()

            # Check input (TODO)

            # Wait
            sleep(self._waitTime)



    def run(self, stdscr):
        # TODO: Maybe remove the wrapper in befish.py 
        #       and handle errors here instead
        #       There's already a _deinit function
        self._init()
        self._wrappedRun()
        self._cursorLocation[1] = 0
        self._stdscr.addstr(*self._cursorLocation, "End of Execution.")
        self._deinit()

    def _deinit(self):
        self._stdscr.getkey()
        curses.nocbreak()
        curses.echo()
        curses.curs_set(True)
        self._stdscr.keypad(False)
        curses.endwin()
