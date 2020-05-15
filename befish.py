import sys
from time import sleep
from engine import *
from debug import *


if __name__ == "__main__":
    code = debugInterpreter(sys.argv[1])
    # for line in code._code:
    #     for char in line:
    #         print(chr(char), end="")
    #     print()
    code.run()
