import sys

from step1 import reader
from step1 import printer


def READ(str_):
    return reader.read_str(str_)


def EVAL(ast, env):
    return ast


def PRINT(exp):
    return printer.print_str(exp)


def rep(str_):
    return PRINT(EVAL(READ(str_), ""))


def readline(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def main():
    while True:
        try:
            print(rep(readline("user> ")))
        except Exception as err:
            print(err)


if __name__ == "__main__":
    main()
