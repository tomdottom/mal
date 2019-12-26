from mal_types import Symbol, List, Array, String, HashMap


def pr_str(exp):
    if isinstance(exp, Symbol):
        return str(exp)
    elif isinstance(exp, int):
        return str(exp)
    elif isinstance(exp, List):
        return "(" + " ".join([pr_str(e) for e in exp]) + ")"
    elif isinstance(exp, Array):
        return "[" + " ".join([pr_str(e) for e in exp]) + "]"
    elif isinstance(exp, HashMap):
        return "{" + " ".join([f"{pr_str(k)} {pr_str(v)}" for k, v in exp.items()]) + "}"
    elif isinstance(exp, String):
        return f'"{exp}"'
    else:
        raise Exception("Bar")
