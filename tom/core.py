import mal_types
import printer


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

ns = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: int(a / b),

    "pr-str": pr_str,
    "prn": prn,
    "println": prn_ln,
    "str": str_,
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