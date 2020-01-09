from mal_types import Symbol, List, Array, String, HashMap, Function, Keyword, Atom, Comment


def _escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')


def pr_str(exp, print_readably=True):
    if isinstance(exp, Symbol):
        return String(exp)
    elif exp is True:
        return String("true")
    elif exp is False:
        return String("false")
    elif exp is None:
        return String("nil")
    elif isinstance(exp, int):
        return String(exp)
    elif isinstance(exp, List):
        return String("(" + " ".join([pr_str(e, print_readably=print_readably) for e in exp]) + ")")
    elif isinstance(exp, Array):
        return String("[" + " ".join([pr_str(e, print_readably=print_readably) for e in exp]) + "]")
    elif isinstance(exp, HashMap):
        return String("{" + " ".join([f"{pr_str(k, print_readably=print_readably)} {pr_str(v, print_readably=print_readably)}" for k, v in exp.items()]) + "}")
    elif isinstance(exp, String):
        if print_readably:
            return String(f'"{_escape(exp)}"')
        return exp
    elif isinstance(exp, Atom):
        return f"(atom {pr_str(exp.ref)})"
    elif isinstance(exp, Keyword):
        return String(exp)
    elif isinstance(exp, Function):
        return String("#<function>")
    elif isinstance(exp, Comment):
        return String(exp)
    elif callable(exp):
        return String("#<function>")
    else:
        raise Exception(f"Do not know how to print expression: {exp}")
