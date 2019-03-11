import random
from collections import Counter


class Engine:
    def __init__(self):
        self.units = []
        self.tick: int = 0

    def select_target(self, unit):
        platoon = unit.platoon
        targets = [x for x in self.units if x.life.raw > 0 and x.platoon != platoon]
        return random.choice(targets) if targets else None

    def check_for_end(self) -> bool:
        return len(Counter([x.platoon for x in self.units])) > 1

    def turn(self):
        self.tick += 1
        for unit in self.units:
            if unit.life.raw <= 0:
                continue
            target = self.select_target(unit)
            if target is None:
                continue
            unit.damage_to(target)
        self.units = [x for x in self.units if x.life.raw > 0]

    def print_units(self):
        print("turn: {}".format(self.tick))
        for unit in self.units:
            print("{}".format(unit))
        print()

    def print_winner(self):
        print("turn: {}".format(self.tick))
        print("winner platoon {}".format(self.units[0].platoon))
        print("{}".format([t.life.native for t in self.units[0].targets]))


def main():
    eng = Engine()
    from unit import new_unit

    p = new_unit("player", 100, 15, 5, "blue", "human")
    eng.units.append(p)
    for x in range(random.randint(5, 10)):
        life = random.randint(10, 20)
        u = new_unit(
            "demon{}".format(x),
            life,
            random.randint(1, 10),
            random.randint(1, 10),
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
            random.randint(1, 10),
            random.randint(1, 10),
            "green",
            "fish",
            life + 10,
        )
        eng.units.append(u)
    while eng.check_for_end():
        eng.print_units()
        eng.turn()
    eng.print_winner()


if __name__ == "__main__":
    main()
