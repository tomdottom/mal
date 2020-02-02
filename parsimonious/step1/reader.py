import sys
import textwrap
import os

from parsimonious.grammar import Grammar

from .visitor import MalVisitor

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
GRAMMAR_FILE = os.path.join(FILE_DIR, "./step1_read_print.grammar")


with open(GRAMMAR_FILE) as fh:
    grammar = Grammar(fh.read())


visitor = MalVisitor()


def read_str(str_):
    try:
        ast = grammar.parse(str_)
        return visitor.visit(ast)
    except Exception as err:
        if err.expr.name == "RIGHT_PAREN":
            raise Exception(textwrap.dedent(f"""
                Error: unbalanced parenthesis in on line {err.line()} column {err.column()}
                {err.text}
                {" " * err.column() + "^"}
            """).strip())
        elif err.expr.name == "RIGHT_BRACKET":
            raise Exception(textwrap.dedent(f"""
                Error: unbalanced bracket in on line {err.line()} column {err.column()}
                {err.text}
                {" " * err.column() + "^"}
            """).strip())
        elif err.expr.name == "CLOSE_QUOTE":
            raise Exception(textwrap.dedent(f"""
                Error: unbalanced quote in on line {err.line()} column {err.column()}
                {err.text}
                {" " * err.column() + "^"}
            """).strip())
        else:
            raise Exception(f"Error: {err}")
