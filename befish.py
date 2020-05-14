import sys
from time import sleep
from engine import *


class StopExecution(Exception):
    # Halt execution when an error pops up or it has reached the end
    def __init__(self, message=None):
        self.message = message

if __name__ == "__main__":
    code = Interpreter(sys.argv[1], False)
    for line in code._code:
        for char in line:
            print(chr(char), end="")
        print()
    code._run()
    # print(code._currentStack)
    # print(code._output)
