import operator as op
import sys

import mal_types
import printer
import reader
import env as env_module
import core


def READ(str):
    return reader.read_str(str)


def eval_ast(ast, env):
    if isinstance(ast, mal_types.Symbol):
        try:
            return env.get(ast)
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


def EVAL(ast, env, _stats={'depth': 0, 'loop': 0}):
    _stats['depth'] += 1

    while True:
        _stats['loop'] += 1
        # if _stats['depth'] > 10:
        #     import pudb; pudb.set_trace()
        if not isinstance(ast, mal_types.List):
            _stats['depth'] -= 1
            return eval_ast(ast, env)

        if len(ast) == 0:
            _stats['depth'] -= 1
            return ast

        a0 = ast[0]

        if a0 == "def!":
            a1, a2 = ast[1:3]
            _stats['depth'] -= 1
            return env.set(a1, EVAL(a2, env))

        if a0 == "let*":
            a1, a2 = ast[1:3]
            let_env = env_module.Env(outer=env)
            for i in range(0, len(a1), 2):
                k = a1[i]
                v = EVAL(a1[i+1], let_env)
                let_env.set(k, v)

            # return EVAL(a2, let_env)
            env = let_env
            ast = a2

            continue

        if a0 == "do":
            el = eval_ast(mal_types.List(ast[1:-1]), env)
            ast = ast[-1]
            # for a in ast[1:]:
            #     value = EVAL(a, env)
            # return value
            continue

        if a0 == "fn*":
            params, ast = ast[1:3]

            def fn(*args, params=params, ast=ast):
                try:
                    args = mal_types.List(args)
                    vargs_index = params.index('&')
                    params = mal_types.List(params[:vargs_index] + params[vargs_index + 1:])
                    rest = args[vargs_index:]
                    args = mal_types.List(args[:vargs_index])
                    args.append(mal_types.List(rest))
                except ValueError:
                    pass

                if_env = env_module.Env(
                    outer=env,
                    binds=params,
                    exprs=args,
                )
                return EVAL(ast, if_env)

            fn = mal_types.Function(fn)
            fn.__ast__ = ast
            fn.__env__ = env
            fn.__params__ = params

            _stats['depth'] -= 1
            return fn

        if a0 == "if":
            a1 = ast[1]
            result = EVAL(a1, env)
            if len(ast) < 4:
                return None
            elif result is not None and result is not False:
                a2 = ast[2]
                # return EVAL(a2, env)
                ast = a2
            else:
                a3 = ast[3]
                # return EVAL(a3, env)
                ast = a3

            continue


        el = eval_ast(ast, env)
        fn, args = el[0], el[1:]
        if hasattr(fn, '__ast__'):
            ast = fn.__ast__
            params = fn.__params__
            try:
                args = mal_types.List(args)
                vargs_index = params.index('&')
                params = mal_types.List(params[:vargs_index] + params[vargs_index + 1:])
                rest = args[vargs_index:]
                args = mal_types.List(args[:vargs_index])
                args.append(mal_types.List(rest))
            except ValueError:
                pass

            env = env_module.Env(
                outer=env,
                binds=params,
                exprs=args,
            )
        else:
            _stats['depth'] -= 1
            return fn(*args)



def PRINT(exp):
    return printer.pr_str(exp, True)


ENV = env_module.Env()
for k, v in core.ns.items():
    ENV.set(k, v)


def rep(str):
    return PRINT(EVAL(READ(str), ENV))


def readline(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.readline().strip()


rep("(def! not (fn* (a) (if a false true)))")

if __name__ == "__main__":
    while True:
        try:
            line = readline("user> ")
            if not line:
                break
            print(rep(line))
        except Exception as e:
            import pudb; pudb.set_trace()
            print("Error", e)

