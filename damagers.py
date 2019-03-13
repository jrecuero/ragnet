import math


class Damager:
    def __init__(self, name):
        self.name: str = name
        self.raw: int = 0
        self.blunt: float = 0.0
        self.pierce: float = 0.0
        self.slash: float = 0.0
        self.acc: int = 0

    def __str__(self):
        return "{:3} {:3} [{:3.0f}% {:3.0f}% {:3.0f}%]".format(
            self.raw, self.acc, float(self.slash), float(self.blunt), float(self.pierce)
        )

    def damage_to(self, target: "Defenser") -> int:
        blunt = self.raw * self.blunt / 100.0 - target.raw * target.blunt / 100.0
        pierce = self.raw * self.pierce / 100.0 - target.raw * target.pierce / 100.0
        slash = self.raw * self.slash / 100.0 - target.raw * target.slash / 100.0
        blunt = blunt if blunt > 0 else 0
        pierce = pierce if pierce > 0 else 0
        slash = slash if slash > 0 else 0
        return {
            "damager": self.name,
            "damage": math.ceil(blunt + pierce + slash),
            "acc": self.acc,
            "blunt": blunt,
            "pierce": pierce,
            "slash": slash,
        }


def new_damager(name, raw, acc, blunt=0.0, pierce=0.0, slash=0.0):
    dmgr = Damager(name)
    dmgr.raw = raw
    dmgr.acc = acc
    dmgr.blunt = blunt
    dmgr.pierce = pierce
    dmgr.slash = slash
    return dmgr


def new_scan(raw=100):
    return new_damager("scan", raw, 100, 100.0, 100.0, 100.0)


def new_slasher(raw):
    return new_damager("slasher", raw, 75, slash=100.0)


def new_blunter(raw):
    return new_damager("blunter", raw, 50, blunt=100.0)


def new_piercer(raw):
    return new_damager("piercer", raw, 95, pierce=100.0)
