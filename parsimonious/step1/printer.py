import logging
import os

logger = logging.getLogger(__name__)


def print_str(exp):
    if exp == []:
        logger.debug(f"Empty")
        return ""
    if exp.type == "Number":
        logger.debug(f"Number({exp.value})")
        return str(exp.value)
    elif exp.type == "Symbol":
        logger.debug(f"Symbol({exp.value})")
        return exp.value
    elif exp.type == "Keyword":
        logger.debug(f"Keyword({exp.value})")
        return f":{exp.value}"
    elif exp.type == "String":
        logger.debug(f"String({exp.value})")
        return f'"{exp.value}"'
    elif exp.type == "List":
        children = " ".join(print_str(c) for c in exp.children)
        logger.debug(f"List({children})")
        return f"({children})"
    elif exp.type == "Vector":
        children = " ".join(print_str(c) for c in exp.children)
        logger.debug(f"Vector({children})")
        return f"[{children}]"
    elif exp.type == "HashMap":
        children = " ".join(print_str(c) for kv in exp.children for c in kv)
        logger.debug(f"HashMap({children})")
        return f"{{{children}}}"
    else:
        raise Exception(f"Don't know how to represent {exp}")
