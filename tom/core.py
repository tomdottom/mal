import mal_types
import printer
import reader


def pr_str(*exp, print_readably=True, join_str=" "):
    return mal_types.String(join_str.join(
        printer.pr_str(e, print_readably=print_readably)
        for e in exp
    ))


def prn(*exp):
    print(pr_str(*exp, print_readably=True, join_str=" "))
    return None


def prn_ln(*exp):
    print(pr_str(*exp, print_readably=False))
    return None


def str_(*exp):
    return pr_str(*exp, print_readably=False, join_str="")


def lst(*exp):
    return mal_types.List(exp)


def is_lst(exp):
    return isinstance(exp, mal_types.List)


def is_empty(exp):
    if isinstance(exp, mal_types.List):
        return len(exp) == 0
    if isinstance(exp, mal_types.Array):
        return len(exp) == 0
    return False


def count(exp):
    if exp is None:
        return 0
    return len(exp)


def gt(a, b):
    return a > b


def lt(a, b):
    return a < b


def gte(a, b):
    return a >= b


def lte(a, b):
    return a <= b


def eq(a, b):
    if type(a) == type(b):
        return a == b
    collection_types = (mal_types.List, mal_types.Array)
    if isinstance(a, collection_types) and isinstance(b, collection_types):
        if len(a) == len(b):
            for a, b in zip(a, b):
                if a != b:
                    return False
            return True

    return False


def read_string(str):
    return reader.read_str(str)


def slurp(str):
    with open(str) as fh:
        contents = fh.read()
    return mal_types.String(contents)


def reset(atom, value):
    atom.ref = value
    return value


ns = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: int(a / b),

    "atom": lambda ref: mal_types.Atom(ref),
    "atom?": lambda x: isinstance(x, mal_types.Atom),
    "deref": lambda atom: atom.ref,
    "reset!": reset,

    "pr-str": pr_str,
    "prn": prn,
    "println": prn_ln,

    "str": str_,
    "read-string": read_string,

    "slurp": slurp,

    "list": lst,
    "list?": is_lst,
    "empty?": is_empty,
    "count": count,

    ">": gt,
    "<": lt,
    ">=": gte,
    "<=": lte,
    "=": eq,
}

defs = [
    "(def! not (fn* (a) (if a false true)))",
    "(def! load-file (fn* (path) (eval (read-string (str \"(do \" (slurp path) \" \nnil )\")))))",
    # "(def! swap! (fn* (a f & args) (do (reset! a (f (deref a) args)) (deref a))))",
]