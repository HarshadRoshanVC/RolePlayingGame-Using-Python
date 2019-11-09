import random

class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    def generate_damage(self):
        self.low = self.dmg - 15
        self.high = self.dmg + 15
        return random.randrange(self.low,self.high)
    
