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


class Defenser:
    def __init__(self):
        self.raw = 0
        self.blunt = 0.0
        self.pierce = 0.0
        self.slash = 0.0

    def __str__(self):
        return "{:3} [{:3.0f}% {:3.0f}% {:3.0f}%]".format(
            self.raw, float(self.slash), float(self.blunt), float(self.pierce)
        )


def new_defenser(raw, blunt=0.0, pierce=0.0, slash=0.0):
    defr = Defenser()
    defr.raw = raw
    defr.blunt = blunt
    defr.pierce = pierce
    defr.slash = slash
    return defr
