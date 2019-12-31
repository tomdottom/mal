class Env(dict):
    MISSING = object()

    def __init__(self, outer=None, binds=[], exprs=[]):
        self.data = {}
        self.outer = outer
        for k, v in zip(binds, exprs):
            self.data[k] = v

    def set(self, symbol, value):
        self.data[symbol] = value
        return value

    def find(self, symbol):
        _env = self
        while True:
            if symbol in _env.data:
                return _env.data[symbol]

            if _env.outer is None:
                return self.MISSING

            _env = _env.outer

    def get(self, symbol):
        value = self.find(symbol)
        if value is not self.MISSING:
            return value

        raise Exception(f"{symbol} not found")
