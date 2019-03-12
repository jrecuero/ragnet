class Damager:
    def __init__(self, name):
        self.name = name
        self.raw = 0
        self.blunt = 0.0
        self.pierce = 0.0
        self.slash = 0.0

    def __str__(self):
        return "{:3} [{:3.0f}% {:3.0f}% {:3.0f}%]".format(
            self.raw, float(self.slash), float(self.blunt), float(self.pierce)
        )

    def damage_to(self, target: "Defenser") -> int:
        blunt = self.raw * self.blunt / 100.0 - target.raw * target.blunt / 100.0
        pierce = self.raw * self.pierce / 100.0 - target.raw * target.pierce / 100.0
        slash = self.raw * self.slash / 100.0 - target.raw * target.slash / 100.0
        return {
            "damager": self.name,
            "damage": int(blunt + pierce + slash),
            "blunt": blunt,
            "pierce": pierce,
            "slash": slash,
        }


def new_damager(name, raw, blunt=0.0, pierce=0.0, slash=0.0):
    dmgr = Damager(name)
    dmgr.raw = raw
    dmgr.blunt = blunt
    dmgr.pierce = pierce
    dmgr.slash = slash
    return dmgr


def new_scan(raw=100):
    return new_damager("scan", raw, 100.0, 100.0, 100.0)
