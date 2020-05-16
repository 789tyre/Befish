import argparse
from engine import *
from debug import *
from curses import wrapper


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="(Enter description here)",
            prog="befish",
            usage="%(prog)s (filename) [options]"
        )
    parser.add_argument("file", help="Path to file that contains the program")
    parser.add_argument("-d", "--debug", help="Used to debug your program", action="store_true")
    parser.add_argument("-t", "--time", help="Time to wait before the next instruction is executed. The default is 0.25s", default=0.25, type=float)
    args = parser.parse_args()

    if args.debug:
        code = debugInterpreter(args.file, args.time)
    else:
        code = Interpreter(args.file)

    wrapper(code.run)
