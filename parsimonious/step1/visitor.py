from typing import Optional
import dataclasses
import itertools
import logging

# logging.basicConfig(level=logging.DEBUG)

import parsimonious


def flatten(list_of_lists):
    return itertools.chain(*list_of_lists)


@dataclasses.dataclass
class AstNode:
    type: str
    value: Optional[str]
    children: Optional[list]


class MalVisitor(parsimonious.NodeVisitor):
    PASS_THRU_EXPRESSIONS = {
        "List", "Vector", "HashMap",
        "Number", "Symbol", "Keyword", "String",
    }

    def visit_EXPRESSION(self, node, visited_children):
        expression_list, _, _ = visited_children
        expression_ = expression_list[0]
        if expression_.type in self.PASS_THRU_EXPRESSIONS:
            return expression_
        elif expression_.type == "Comment":
            return []
        # Unwrap Whitespace
        elif expression_.type == "WhiteSpace":
            return expression_.children
        else:
            import pudb; pudb.set_trace()

    def visit_LIST(self, node, visited_children):
        return AstNode(type="List", value=None, children=[c for c in flatten(visited_children) if c != []])

    def visit_VECTOR(self, node, visited_children):
        return AstNode(type="Vector", value=None, children=[c for c in flatten(visited_children) if c != []])

    def visit_HASHMAP(self, node, visited_children):
        children = list(
            tuple(kvdata)
            for kvdata in flatten(visited_children)
            if isinstance(kvdata, list)
        )
        return AstNode(type="HashMap", value=None, children=children)

    def visit_HASHMAP_KEY(self, node, visited_children):
        key = (key, ), _ = visited_children
        return key

    def visit_NUMBER(self, node, visited_children):
        return AstNode(type="Number", value=int(node.text), children=None)

    def visit_SYMBOL(self, node, visited_children):
        return AstNode(type="Symbol", value=node.text.strip(), children=None)

    def visit_KEYWORD(self, node, visited_children):
        return AstNode(type="Keyword", value=node.text.strip()[1:], children=None)

    def visit_STRING(self, node, visited_children):
        return AstNode(type="String", value=node.text.strip('"'), children=None)

    def _convert_to_list(self, value, *children):
        return AstNode(
            type="List",
            value=None,
            children=[
                AstNode(type="Symbol", value=value, children=None),
                *children
            ]
        )

    def visit_QUOTED(self, node, visited_children):
        _, expr = visited_children
        return self._convert_to_list("quote", expr)

    def visit_QUASI_QUOTED(self, node, visited_children):
        _, expr = visited_children
        return self._convert_to_list("quasiquote", expr)

    def visit_SPLICE_UNQUOTED(self, node, visited_children):
        _, expr = visited_children
        return self._convert_to_list("splice-unquote", expr)

    def visit_UNQUOTED(self, node, visited_children):
        _, expr = visited_children
        return self._convert_to_list("unquote", expr)

    def visit_DEREFED(self, node, visited_children):
        _, expr = visited_children
        return self._convert_to_list("deref", expr)

    def visit_META(self, node, visited_children):
        _, expr, meta = visited_children
        return self._convert_to_list("with-meta", meta, expr)

    def visit_COMMENT(self, node, visited_children):
        return AstNode(type="Comment", value="", children=visited_children)

    def visit_WHITE_SPACE(self, node, visited_children):
        return AstNode(type="WhiteSpace", value="", children=visited_children)

    def generic_visit(self, node, visited_children):
        return visited_children
