from random import choice
unit_types = ["Sword","Bow","Staff"]
inventory = {x:0 for x in unit_types}

class unit:
    def __init__(self, type,strength=1):
        self.type = type
        self.strength = strength


def genUnits():
    for _ in range(2**1024):
        newUnit = unit(choice(unit_types))
        yield newUnit #lazy gen so we can go on indefintly

generator = genUnits()#gens new users
