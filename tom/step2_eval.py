import sys

import mal_types
import printer
import reader


def READ(str):
    return reader.read_str(str)


def eval_ast(ast, env):
    if isinstance(ast, mal_types.Symbol):
        try:
            return env[ast]
        except KeyError:
            raise Exception(f"'{ast}' not found'")

    if isinstance(ast, mal_types.List):
        return mal_types.List((
            EVAL(x, env)
            for x in ast
        ))

    if isinstance(ast, mal_types.Array):
        return mal_types.Array((
            EVAL(x, env)
            for x in ast
        ))

    if isinstance(ast, mal_types.HashMap):
        return mal_types.HashMap((
            (k, EVAL(v, env))
            for k, v in ast.items()
        ))

    return ast


def EVAL(ast, env):
    if not isinstance(ast, mal_types.List):
        return eval_ast(ast, env)

    if len(ast) == 0:
        return ast

    el = eval_ast(ast, env)
    fn, args = el[0], el[1:]
    return fn(*args)



def PRINT(exp):
    return printer.pr_str(exp)


ENV = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: int(a / b),
}


def rep(str):
    return PRINT(EVAL(READ(str), ENV))


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

