from collections import OrderedDict
import random
from base import Base, Stat, Defenser
from damagers import Damager


class Unit(Base):
    def __init__(self, name):
        super(Unit, self).__init__(name)
        self.life: Stat = None
        self.damagers: List[Damager] = []
        self.defenser: Defenser = None
        self.pdmg: Stat = None
        self.pdef: Stat = None
        self.xp: int = 0
        self.level: int = 1
        self.xp_for_kill: int = 0
        self.platoon: str = None
        self.klass: str = None
        self._targets = OrderedDict()

    def __str__(self):
        damagerStr = " ".join([str(x) for x in self.damagers])
        return "[{:2}] | {:8} ({:2}|{:3}) | {:8} | {:8} | {:3} | {:3} {} | {} -> t:{:8}".format(
            self.id,
            self.name,
            self.level,
            self.xp,
            self.platoon,
            self.klass,
            self.life.raw,
            self.pdmg.raw,
            damagerStr,
            self.defenser,
            list(self._targets.keys())[-1].name if len(self._targets) else "None",
        )

    @property
    def targets(self):
        return list(self._targets.keys())

    def is_alive(self):
        return self.life.raw > 0

    def level_up(self):
        while self.xp > 50 * self.level:
            self.life.level_up(self.level)
            self.pdmg.level_up(self.level)
            for damager in self.damagers:
                damager.raw += self.pdmg.delta(0)
            self.pdef.level_up(self.level)
            self.defenser.raw = self.pdef.raw
            self.level += 1

    def damage_to(self, target):
        damage = {"damage": 0}
        for damager in self.damagers:
            dmg = damager.damage_to(target.defenser)
            if dmg["damage"] > damage["damage"]:
                damage = dmg
        if damage["damage"] > 0:
            target.life.raw -= damage["damage"]
        damage.update({"klass": target.klass, "target": target.name})
        self._targets.setdefault(target, []).append(damage)
        if not target.is_alive():
            self.xp += target.xp_for_kill
        self.level_up()


def new_unit(name, life, damagers, defenser, platoon, klass, xp=10) -> Unit:
    unit = Unit(name)
    unit.life = Stat(life, lambda x: 10)
    unit.damagers = damagers
    unit.pdmg = Stat(0, lambda x: 2)
    unit.defenser = defenser
    unit.pdef = Stat(defenser.raw, lambda x: 1)
    unit.platoon = platoon
    unit.klass = klass
    unit.xp_for_kill = xp
    return unit
