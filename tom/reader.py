import re

from mal_types import Symbol, List, Array, String, HashMap, Keyword, Comment


class Reader:
    def __init__(self, tokens=[]):
        self.tokens = tokens
        self.current_position = 0
        self.max_index = len(self.tokens) - 1

    def next(self):
        token = self.tokens[self.current_position]
        self.current_position += 1
        return token

    def peek(self):
        if self.current_position > self.max_index:
            return None
        token = self.tokens[self.current_position]
        return token


def read_str(str):
    return read_form(Reader(tokenize(str)))


TOKENIZER = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)""")

def tokenize(str):
    return [t for t in TOKENIZER.findall(str) if t != ""]


def read_form(reader):
    token = reader.peek()
    if token[0] == ";":
        reader.next()
        return Comment(token)
    if token == "'":
        reader.next()
        return List((Symbol("quote"), read_form(reader)))
    if token == "`":
        reader.next()
        return List((Symbol("quasiquote"), read_form(reader)))
    if token == "~@":
        reader.next()
        return List((Symbol("splice-unquote"), read_form(reader)))
    if token == "~":
        reader.next()
        return List((Symbol("unquote"), read_form(reader)))
    if token == "@":
        reader.next()
        return List((Symbol("deref"), read_form(reader)))
    if token == "^":
        reader.next()
        metadata = read_form(reader)
        data = read_form(reader)
        return List((Symbol("with-meta"), data, metadata))
    if token == "(":
        return read_list(reader)
    if token == "[":
        return read_array(reader)
    if token == "{":
        return read_hash_map(reader)
    else:
        return read_atom(reader)


def read_sequence(reader, typ, start, end):
    ast = typ()

    token = reader.next()
    if token != start:
        raise Exception(f"Expected, {start}")

    token = reader.peek()
    while token != end:
        if token is None:
            raise Exception(f"Expected {end}, for EOF")
        ast.append(read_form(reader))
        token = reader.peek()

    reader.next()

    return ast


def read_list(reader):
    return read_sequence(reader, List, "(", ")")


def read_array(reader):
    return read_sequence(reader, Array, "[", "]")


def read_hash_map(reader):
    lst = read_sequence(reader, Array, "{", "}")
    return HashMap((
        (lst[i], lst[i+1])
        for i in range(0, len(lst), 2)
    ))


INT_RE = re.compile(r"-?[0-9]+$")
STRING_RE = re.compile(r'"(?:[\\].|[^\\"])*"')


def _unescape(s):
    return s.replace('\\\\', '\u029e').replace('\\"', '"').replace('\\n', '\n').replace('\u029e', '\\')


def read_atom(reader):
    token = reader.next()
    if re.match(INT_RE, token):
        return int(token)

    if re.match(STRING_RE, token):
        return String(_unescape(token[1:-1]))
    if token[0] == '"':
        raise Exception('Expected \'"\', found EOF')
    if token[0] == ':':
        return Keyword(token)
    if token == "true":
        return True
    if token == "false":
        return False
    if token == "nil":
        return None
    else:
        return Symbol(token)

