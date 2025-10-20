from random import choice
unit_types = ["Sword","Bow","Staff"]
inventory = {x:0 for x in unit_types}

class unit:
    def __init__(self, type,hp:float=100.0):
        self.type:str = type
        self.hp:float = hp

    def damage(self,dmg:float)->bool:
        self.hp-=dmg
        return self.hp>0

    def __repr__(self)->str:
        return f"Unit of type: {self.type} with {self.hp}"

def genUnits():
    for _ in range(2**1024):
        newUnit = unit(choice(unit_types))
        yield newUnit #lazy gen so we can go on indefintly

generator = genUnits()#gens new users
