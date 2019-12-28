class Env(dict):
    def __init__(self, outer=None):
        self.outer = outer

    def set(self, symbol, value):
        self[symbol] = value
        return value

    def find(self, symbol):
        try:
            value = self[symbol]
        except KeyError:
            value = None
        if value is not None:
            return value
        if self.outer is not None:
            return self.outer.find(symbol)

    def get(self, symbol):
        value = self.find(symbol)
        if value is not None:
            return value

        raise Exception(f"{symbol} not found")
