class Atom:
    def __init__(self, ref):
        self.ref = ref


class Symbol(str): pass


class Keyword(str): pass


class List(list): pass


class Array(list): pass


class String(str): pass


class HashMap(dict): pass


class Function:
    def __init__(self, fn):
        self.fn = fn
    def __call__(self, *args):
        return self.fn(*args)


class Comment(str):
    pass
