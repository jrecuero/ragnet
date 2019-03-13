import random
from collections import Counter
from base import new_defenser
from damagers import new_damager, new_slasher, new_blunter, new_piercer


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
            # if not unit.is_alive():
            #     continue
            if not unit.engaged or not unit.engaged.is_alive():
                unit.engaged = None
                target = self.select_target(unit)
            else:
                target = unit.engaged
            if target is None:
                continue
            if not unit.engaged and not target.engaged:
                unit.engaged = target
                target.engaged = unit
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
        stats = {}
        pds = []
        for k, dmgs in self.units[0]._targets.items():
            stats.setdefault(k.klass, []).extend(dmgs)
            pds.extend(dmgs)
        for k, dmgs in stats.items():
            print(k)
            for d in dmgs:
                print("\t{}".format(d))
        import pandas

        df = pandas.DataFrame(pds)
        df = df[
            [
                "klass",
                "target",
                "damager",
                "damage",
                "acc",
                "to-hit",
                "hit",
                "slash",
                "blunt",
                "pierce",
            ]
        ]
        print(df)


def main():
    eng = Engine()
    from unit import new_unit

    def generate_player():
        return new_unit(
            "player",
            random.randint(100, 200),
            10,
            10,
            [
                new_slasher(random.randint(15, 20)),
                new_blunter(random.randint(30, 50)),
                new_piercer(random.randint(5, 10)),
            ],
            new_defenser(
                random.randint(5, 10),
                slash=random.randint(1, 50),
                blunt=random.randint(1, 50),
                pierce=random.randint(1, 50),
            ),
            "blue",
            "human",
        )

    def generate_demons():
        demons = []
        for x in range(random.randint(5, 10)):
            life = random.randint(40, 50)
            u = new_unit(
                "demon{}".format(x),
                life,
                5,
                5,
                [
                    new_damager(
                        "weapon",
                        random.randint(1, 10),
                        75,
                        slash=random.randint(25, 50),
                        blunt=random.randint(1, 25),
                        pierce=random.randint(25, 50),
                    )
                ],
                new_defenser(random.randint(1, 10), slash=100, blunt=0, pierce=100),
                "red",
                "demon",
                life + 10,
            )
            demons.append(u)
        return demons

    def generate_fishes():
        fishes = []
        for x in range(random.randint(5, 10)):
            life = random.randint(20, 40)
            u = new_unit(
                "fish{}".format(x),
                life,
                5,
                5,
                [
                    new_damager(
                        "weapon",
                        random.randint(1, 10),
                        75,
                        slash=random.randint(1, 25),
                        blunt=random.randint(25, 50),
                        pierce=random.randint(25, 50),
                    )
                ],
                new_defenser(random.randint(1, 10), slash=0, blunt=100, pierce=100),
                "green",
                "fish",
                life + 10,
            )
            fishes.append(u)
        return fishes

    def generate_birds():
        birds = []
        for x in range(random.randint(5, 10)):
            life = random.randint(25, 40)
            u = new_unit(
                "bird{}".format(x),
                life,
                5,
                5,
                [
                    new_damager(
                        "weapon",
                        random.randint(1, 10),
                        75,
                        slash=random.randint(25, 50),
                        blunt=random.randint(25, 50),
                        pierce=random.randint(1, 10),
                    )
                ],
                new_defenser(random.randint(1, 10), slash=100, blunt=100, pierce=0),
                "yellow",
                "bird",
                life + 10,
            )
            birds.append(u)
        return birds

    eng.units.append(generate_player())
    eng.units.extend(generate_demons())
    eng.units.extend(generate_fishes())
    eng.units.extend(generate_birds())
    while eng.check_for_end():
        eng.print_units()
        eng.turn()
    eng.print_winner()


if __name__ == "__main__":
    main()
