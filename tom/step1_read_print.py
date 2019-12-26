import sys

import reader
import printer


def READ(str):
    return reader.read_str(str)


def EVAL(ast, env):
    return ast


def PRINT(exp):
    return printer.pr_str(exp)


def rep(str):
    return PRINT(EVAL(READ(str), {}))


def readline(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.readline().strip()


if __name__ == "__main__":
    while True:
        try:
            line = readline("user> ")
            if not line:
                break
            print(rep(line))
        except Exception as e:
            print("Error", e)

