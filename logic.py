from random import choice

class unit:
    def __init__(self, type,strength=1):
        self.type = type
        self.strength = strength

unit_types = ["sword","bow","staff"]

def genUnits():
    for _ in range(2**1024):
        newUnit = unit(choice(unit_types))
        yield newUnit #lazy gen so we can go on indefintly

generator = genUnits()#gens new users
