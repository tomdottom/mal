import sys


def READ(str_):
    return str_


def EVAL(ast, env):
    return ast


def PRINT(exp):
    return exp


def rep(str_):
    return PRINT(EVAL(READ(str_), ""))


def readline(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.readline().strip()
    pass


def main():
    while True:
        print(rep(readline("user> ")))


if __name__ == "__main__":
    main()
