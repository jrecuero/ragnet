from base import Base, Stat


class Unit(Base):
    def __init__(self, name):
        super(Unit, self).__init__(name)
        self.life: Stat = None
        self.damage: int = 0
        self.defense: int = 0
        self.xp: int = 0
        self.level: int = 1
        self.xp_for_kill: int = 0
        self.platoon: str = None
        self.klass: str = None
        self.targets = []
        self.last_target = None

    def __str__(self):
        return "[{:2}] {:8} {:8} | l.{:3} | D.{:2} | d.{:2} | {:8}  xp.{:3} -> t:{:8}".format(
            self.id,
            self.name,
            self.platoon,
            self.life.raw,
            self.damage,
            self.defense,
            self.klass,
            self.xp,
            self.last_target.name if self.last_target else "None",
        )

    def damage_to(self, target):
        self.last_target = target
        if target not in self.targets:
            self.targets.append(target)
        damage = self.damage - target.defense
        if damage > 0:
            target.life.raw -= damage
        if target.life.raw <= 0:
            self.xp += target.xp_for_kill
        if self.xp > 50 * self.level:
            self.life.level_up(self.level)
            self.level += 1


def new_unit(name, life, damage, defense, platoon, klass, xp=10) -> Unit:
    unit = Unit(name)
    unit.life = Stat(life, lambda x: 10)
    unit.damage = damage
    unit.defense = defense
    unit.platoon = platoon
    unit.klass = klass
    unit.xp_for_kill = xp
    return unit
