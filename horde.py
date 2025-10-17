HORDEMAXHEALTH =  10_000
HORDELVLUP = 5

BOSSMAXHEALTH = 10_000 #macros for boss and horde. Leaving here so rebalancing will be easy
BOSSDAMAGE = 10 #DPS that boss does to your troops/horde bar

class boss:
    def __init__(self,type):
        self.hp = BOSSMAXHEALTH
        self.type = type
        self.strength =  BOSSDAMAGE

    '''
    returns None of no damage was done to boss, and the boss will in fact attack you
    or an float representing the remaining health if dmg was done to boss as a percent
    '''
    def attack(self,dmg:int)->int|float:
        if dmg<=0:
           return int(self.strength) #does dmg to your horde bar
        self.hp-= dmg
        return float(self.hp/BOSSMAXHEALTH) #set new health %

    def attackTopps(self)->int:
        return self.strength



class horde:

    def __init__(self):
        self.dps = 0
        self.hp = 0

    '''
    returns int if no damage was done to horde and the int represents dmg to do to troops,
    or a float representing the remaining health if dmg was done to boss as a percent
    '''
    def progress(self)->float:
        self.hp+=self.dps
        return self.hp/HORDEMAXHEALTH

    def noProgress(self)->int:
        return self.dps

    def increaseDifficulty(self):
        self.dps+=HORDELVLUP
