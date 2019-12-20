import sys


def READ(str):
    return str


def EVAL(ast, env):
    return ast


def PRINT(exp):
    return exp


def rep(str):
    return PRINT(EVAL(READ(str), {}))


def readline(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.readline().strip()


if __name__ == "__main__":
    while True:
        line = readline("user> ")
        if not line:
            break
        print(rep(line))

