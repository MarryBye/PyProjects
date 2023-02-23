from random import randint, uniform, shuffle


class Hero:
    def __init__(self, name, health, armor, damage):
        self.name = name
        self.health = health
        self.maxHealth = health
        self.armor = armor
        self.maxArmor = armor
        self.damage = damage

        self.uniqueID = randint(1000000, 9999999)
        self.minDamage = self.damage * 0.5
        self.maxDamage = self.damage * 1.5

    def get_stats(self):
        print("\n")
        print(f"СТАТИСТИКА ИГРОКА {self.uniqueID}")
        print(f"Имя героя: {self.name}")
        print(f"Здоровье героя: {self.health} / {self.maxHealth}")
        print(f"Броня героя: {self.armor} / {self.maxArmor}")
        print(f"Урон героя: {self.minDamage} - {self.maxDamage} ({self.damage})")

    def alive(self):
        return self.health > 0

    def regen(self):
        self.health = self.maxHealth
        self.armor = self.maxArmor

    def level_up(self):
        self.maxHealth *= 1.5
        self.maxArmor *= 1.5
        self.damage *= 1.5
        self.minDamage = self.damage * 0.5
        self.maxDamage = self.damage * 1.5
        self.regen()

    def strike(self, char):
        if not self.alive():
            print(f"{self.name} [{self.uniqueID}] мертв!")
            return
        if not char.alive():
            print(f"{char.name} [{char.uniqueID}] мертв!")
            return
        strike_damage = uniform(self.minDamage, self.maxDamage)
        print(f"\n{self.name} [{self.uniqueID}] нанес {strike_damage} урона по {char.name} [{char.uniqueID}]!")
        if char.armor > 0:
            armor_damage = strike_damage * 0.8
            health_damage = strike_damage * 0.2
            char.armor -= armor_damage
            char.health -= health_damage
            print(f"Броня {char.name} [{char.uniqueID}] поглотила {armor_damage} урона!")
        elif char.health > 0:
            char.health -= strike_damage

    def death_fight(self, char):
        if not self.alive():
            print(f"Ваш персонаж мертв!")
            return
        if not char.alive():
            print(f"{char.name} [{char.uniqueID}] мертв!")
            return
        print(f"\nНачалась смертельная битва между {self.name} [{self.uniqueID}] и {char.name} [{char.uniqueID}]!")
        while self.alive() and char.alive():
            do_strike = randint(1, 2)
            if do_strike == 1:
                self.strike(char)
            else:
                char.strike(self)
        else:
            if self.alive():
                winner = self
                loser = char
            elif char.alive():
                winner = char
                loser = self
            print(f"{winner.name} [{winner.uniqueID}] победил {loser.name} [{loser.uniqueID}]!")
            winner.level_up()
            winner.get_stats()
        return winner, loser


def make_prompt(tip, ans, tryAgain, complete):
    question = input(tip)
    while question != ans:
        question = input(tryAgain)
    print(complete)


print("Добро пожаловать в Fortnite")
make_prompt("\nКупить подписку за 299 грн? [yes/no]", "yes", "\nА давай все таки [yes/no]", "Хорош.")
make_prompt("\nЗайти в бой? [yes/no]", "yes", "\nБаттлпас сам себя не пройдет, зайдешь? [yes/no]", "Хорош.")

players = []
for i in range(25):
    players.append(Hero(f"Player{i}", 100, 50, 15))

while len(players) != 1:
    for k, v in enumerate(players):
        if k == len(players) - 1:
            print(f"{v.name} [{v.uniqueID}] избежал всех битв и прошел дальше!")
            shuffle(players)
            break
        winner, loser = v.death_fight(players[k + 1])
        players.remove(loser)
        print(f"Выбыл {loser.name}")

print(f"\nКоролевская победа за игроком {winner.name} [{winner.uniqueID}]!")