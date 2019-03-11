import random
from collections import Counter
from base import new_damager, new_defenser


class Engine:
    def __init__(self):
        self.units = []
        self.tick: int = 0

    def select_target(self, unit):
        platoon = unit.platoon
        targets = [x for x in self.units if x.is_alive() and x.platoon != platoon]
        return random.choice(targets) if targets else None

    def check_for_end(self) -> bool:
        return len(Counter([x.platoon for x in self.units])) > 1

    def turn(self):
        self.tick += 1
        for unit in self.units:
            if not unit.is_alive():
                continue
            target = self.select_target(unit)
            if target is None:
                continue
            unit.damage_to(target)
        self.units = [x for x in self.units if x.is_alive()]

    def print_units(self):
        print("turn: {}".format(self.tick))
        for unit in self.units:
            print("{}".format(unit))
        print()

    def print_winner(self):
        print("turn: {}".format(self.tick))
        for unit in self.units:
            print("winner: {}".format(unit))
        print("{}".format([(t.name, t.life.native) for t in self.units[0].targets]))


def main():
    eng = Engine()
    from unit import new_unit

    p = new_unit(
        "player",
        random.randint(50, 100),
        new_damager(
            "weapon",
            random.randint(10, 20),
            slash=random.randint(25, 50),
            blunt=random.randint(25, 50),
            pierce=random.randint(25, 50),
        ),
        new_defenser(
            random.randint(5, 10),
            slash=random.randint(1, 50),
            blunt=random.randint(1, 50),
            pierce=random.randint(1, 50),
        ),
        "blue",
        "human",
    )
    eng.units.append(p)
    for x in range(random.randint(5, 10)):
        life = random.randint(10, 20)
        u = new_unit(
            "demon{}".format(x),
            life,
            new_damager(
                "weapon",
                random.randint(1, 10),
                slash=random.randint(25, 50),
                blunt=random.randint(1, 25),
                pierce=random.randint(25, 50),
            ),
            new_defenser(
                random.randint(1, 5),
                slash=random.randint(1, 50),
                blunt=random.randint(1, 10),
                pierce=random.randint(1, 50),
            ),
            "red",
            "demon",
            life + 10,
        )
        eng.units.append(u)
    for x in range(random.randint(5, 10)):
        life = random.randint(10, 20)
        u = new_unit(
            "fish{}".format(x),
            life,
            new_damager(
                "weapon",
                random.randint(1, 10),
                slash=random.randint(1, 25),
                blunt=random.randint(25, 50),
                pierce=random.randint(25, 50),
            ),
            new_defenser(
                random.randint(1, 5),
                slash=random.randint(1, 10),
                blunt=random.randint(1, 50),
                pierce=random.randint(1, 50),
            ),
            "green",
            "fish",
            life + 10,
        )
        eng.units.append(u)
    for x in range(random.randint(5, 10)):
        life = random.randint(10, 20)
        u = new_unit(
            "bird{}".format(x),
            life,
            new_damager(
                "weapon",
                random.randint(1, 10),
                slash=random.randint(25, 50),
                blunt=random.randint(25, 50),
                pierce=random.randint(1, 10),
            ),
            new_defenser(
                random.randint(1, 5),
                slash=random.randint(1, 50),
                blunt=random.randint(1, 50),
                pierce=random.randint(0, 0),
            ),
            "yellow",
            "bird",
            life + 10,
        )
        eng.units.append(u)
    while eng.check_for_end():
        eng.print_units()
        eng.turn()
    eng.print_winner()


if __name__ == "__main__":
    main()
