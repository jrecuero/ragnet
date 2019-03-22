from typing import List
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
        self.agi: Stat = None
        self.xp: int = 0
        self.level: int = 1
        self.xp_for_kill: int = 0
        self.platoon: str = None
        self.entente: str = None
        self.klass: str = None
        self._targets = OrderedDict()
        self._last_target: "Unit" = None
        self.engaged: "Unit" = None

    def __str__(self):
        damagerStr = " ".join([str(x) for x in self.damagers])
        return "[{:2}] | {:8} ({:2}|{:3}) | {:8} | {:8} | {:3} | {:3} | {:3} {} | {} -> t:{:8} e:{:8}".format(
            self.id,
            self.name,
            self.level,
            self.xp,
            self.platoon,
            self.klass,
            self.life.raw,
            self.agi.raw,
            self.pdmg.raw,
            damagerStr,
            self.defenser,
            self._last_target.name if self._last_target else "None",
            self.engaged.name if self.engaged else "None",
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
            self.pdef.level_up(self.level)
            self.agi.level_up(self.level)
            self.defenser.raw = self.pdef.raw
            self.level += 1

    def select_damager(self, max_damager, new_damager):
        max_to_hit = max_damager["to-hit"] * max_damager["to-hit"]
        max_damage = max_damager["damage"]
        new_to_hit = new_damager["to-hit"] * new_damager["to-hit"]
        new_damage = new_damager["damage"]
        # max_to_hit = max_damager["to-hit"]
        # max_damage = max_damager["damage"] * max_damager["damage"]
        # new_to_hit = new_damager["to-hit"]
        # new_damage = new_damager["damage"] * new_damager["damage"]
        # if self.name == "player":
        #     print(new_to_hit, new_damage, max_to_hit, max_damage)
        return new_to_hit * new_damage > max_to_hit * max_damage

    def damage_to(self, target):
        damage = {}
        for damager in self.damagers:
            dmg = damager.damage_to(target.defenser)
            dmg["to-hit"] = dmg["acc"] + self.agi.raw - target.agi.raw
            if not damage or self.select_damager(damage, dmg):
                damage = dmg
        damage.update({"klass": target.klass, "target": target.name, "hit": True})
        if random.randint(1, 100) > damage["to-hit"]:
            damage["hit"] = False
        else:
            if damage["damage"] > 0:
                target.life.raw -= damage["damage"]
        self._targets.setdefault(target, []).append(damage)
        self._last_target = target
        if not target.is_alive():
            self.xp += target.xp_for_kill
        self.level_up()


def new_unit(name, life, pdmg, agi, damagers, defenser, platoon, klass, xp=10) -> Unit:
    unit = Unit(name)
    unit.life = Stat(life, lambda x: 10)
    unit.damagers = damagers
    unit.pdmg = Stat(pdmg, lambda x: 2)
    unit.agi = Stat(agi, lambda x: 1)
    unit.defenser = defenser
    unit.pdef = Stat(defenser.raw, lambda x: 1)
    unit.platoon = platoon
    unit.klass = klass
    unit.xp_for_kill = xp
    return unit
