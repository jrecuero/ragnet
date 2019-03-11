class Idier:

    _ID: int = 0

    @classmethod
    def next(cls) -> int:
        cls._ID += 1
        return cls._ID


class Stat:
    def __init__(self, native, delta):
        self.native = native
        self.raw = native
        self.addons = []
        self.delta = delta

    @property
    def max(self):
        _max = self.native
        for x in self.addons:
            _max += x
        return _max

    def level_up(self, level):
        delta = self.delta(level)
        self.native += delta
        self.raw += delta


class Base:
    def __init__(self, name):
        self.name = name
        self.id = Idier.next()
