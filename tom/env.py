class Env(dict):
    MISSING = object()

    def __init__(self, outer=None, binds=[], exprs=[]):
        self.outer = outer
        for k, v in zip(binds, exprs):
            self[k] = v

    def set(self, symbol, value):
        self[symbol] = value
        return value

    def find(self, symbol):
        try:
            value = self[symbol]
        except KeyError:
            value = self.MISSING
        if value is not self.MISSING:
            return value
        if self.outer is not None:
            return self.outer.find(symbol)

    def get(self, symbol):
        value = self.find(symbol)
        if value is not self.MISSING:
            return value

        raise Exception(f"{symbol} not found")
