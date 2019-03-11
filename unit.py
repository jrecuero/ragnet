from collections import OrderedDict
import random
from base import Base, Stat, Damager, Defenser


class Unit(Base):
    def __init__(self, name):
        super(Unit, self).__init__(name)
        self.life: Stat = None
        self.damager: Damager = None
        self.defenser: Defenser = None
        self.pdmg: Stat = None
        self.pdef: Stat = None
        self.xp: int = 0
        self.level: int = 1
        self.xp_for_kill: int = 0
        self.platoon: str = None
        self.klass: str = None
        self._targets = []

    def __str__(self):
        return "[{:2}] | {:8} ({:2}|{:3}) | {:8} | {:8} | {:3} | {} | {} -> t:{:8}".format(
            self.id,
            self.name,
            self.level,
            self.xp,
            self.platoon,
            self.klass,
            self.life.raw,
            self.damager,
            self.defenser,
            self._targets[-1].name if len(self._targets) else "None",
        )

    @property
    def targets(self):
        t = OrderedDict.fromkeys(self._targets)
        return list(t.keys())

    def is_alive(self):
        return self.life.raw > 0

    def level_up(self):
        if self.xp > 50 * self.level:
            self.life.level_up(self.level)
            self.pdmg.level_up(self.level)
            self.damager.raw = self.pdmg.raw
            self.pdef.level_up(self.level)
            self.defenser.raw = self.pdef.raw
            self.level += 1

    def damage_to(self, target):
        self._targets.append(target)
        # pdmg = self.pdmg.raw - target.pdef.raw
        pdmg = self.damager.damage_to(target.defenser)
        if pdmg > 0:
            target.life.raw -= pdmg
        if not target.is_alive():
            self.xp += target.xp_for_kill
        self.level_up()


def new_unit(name, life, damager, defenser, platoon, klass, xp=10) -> Unit:
    unit = Unit(name)
    unit.life = Stat(life, lambda x: 10)
    unit.damager = damager
    unit.pdmg = Stat(damager.raw, lambda x: 2)
    unit.defenser = defenser
    unit.pdef = Stat(defenser.raw, lambda x: 1)
    unit.platoon = platoon
    unit.klass = klass
    unit.xp_for_kill = xp
    return unit
