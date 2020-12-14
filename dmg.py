import game
import random

class Dmg:
    def __init__(self, attacker, defender, atkmethod):


        atklevel = attacker["stats"]["level"]

        if atkmethod == 0 :
            atkstat = attacker["stats"]["atk"] + attacker["weapon"]["atk"]
            defstat = defender["stats"]["def"] + defender["weapon"]["def"]

            critchance = 5 + attacker["stats"]["spe"] + attacker["weapon"]["spe"] - defstat

            critdmg = 2 + 0.05 * atkstat

            rd = random.randint(0, 100)

            if rd <= critchance :
                self.crit = True
                mult = critdmg
            else :
                self.crit = False
                mult = 1

            calcdmg = mult * (((atklevel)/5 + 2) * 2 * (atkstat + 2) / (defstat + 2))

            self.dmg = int(random.randint(88, 100) * calcdmg / 100)




        elif atkmethod == 1 :
            atkstat = attacker["stats"]["spa"] + attacker["weapon"]["spa"]
            defstat = defender["stats"]["spd"] + defender["weapon"]["spd"]

            critchance = 5 + attacker["stats"]["spe"] + attacker["weapon"]["spe"] - (defender["stats"]["def"] + defender["weapon"]["def"])

            critdmg = 2 + 0.05 * (attacker["stats"]["atk"] + attacker["weapon"]["atk"])

            rd = random.randint(0, 100)

            if rd <= critchance :
                self.crit = True
                mult = critdmg
            else :
                self.crit = False
                mult = 1

            calcdmg = mult * (((atklevel)/5 + 2) * 3 * (atkstat + 2) / (defstat + 2))

            self.dmg = int(random.randint(88, 100) * calcdmg / 100)

        else :
            atkstat = max(attacker["stats"]["spa"] + attacker["weapon"]["spa"], attacker["stats"]["atk"] + attacker["weapon"]["atk"])
            defstat = min(defender["stats"]["spd"] + defender["weapon"]["spd"], defender["stats"]["def"] + defender["weapon"]["def"])

            critchance = 15 + attacker["stats"]["spe"] + attacker["weapon"]["spe"] - (defender["stats"]["def"] + defender["weapon"]["def"])

            critdmg = 2 + 0.05 * (attacker["stats"]["atk"] + attacker["weapon"]["atk"])

            rd = random.randint(0, 100)

            if rd <= critchance :
                self.crit = True
                mult = critdmg
            else :
                self.crit = False
                mult = 1

            calcdmg = mult * (((atklevel)/5 + 2) * 2 * (atkstat + 2) / (defstat + 2))

            self.dmg = int(0.65 * random.randint(60, 100) * calcdmg / 100)

        self.dmg = max(1, self.dmg)

