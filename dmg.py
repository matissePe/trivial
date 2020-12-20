import game
import random

class Dmg:
    def __init__(self, attacker, defender, atkmethod):

        atklevel = attacker["stats"]["level"]

        critchance = 5 + attacker["stats"]["spe"] + attacker["weapon"]["spe"] - 0.5 * (defender["stats"]["def"] + defender["weapon"]["def"])

        critdmg = max(2, 2 + 0.05 * (attacker["stats"]["atk"] + attacker["weapon"]["atk"]) - 0.025 *(defender["stats"]["def"] + defender["weapon"]["def"]))

        if atkmethod == 0 :
            atkstat = attacker["stats"]["atk"] + attacker["weapon"]["atk"]
            defstat = defender["stats"]["def"] + defender["weapon"]["def"]


            rd = random.randint(0, 100)

            if rd <= critchance :
                self.crit = True
                mult = critdmg
            else :
                self.crit = False
                mult = 1

            calcdmg = mult * ((((atklevel)/5 + 2) * 2 * (atkstat + 2) + atklevel * 2) / (defstat + 2))

            self.dmg = int(random.randint(88, 100) * calcdmg / 100)




        elif atkmethod == 1 :
            atkstat = attacker["stats"]["spa"] + attacker["weapon"]["spa"]
            defstat = defender["stats"]["spd"] + defender["weapon"]["spd"]


            rd = random.randint(0, 100)

            if rd <= critchance :
                self.crit = True
                mult = critdmg
            else :
                self.crit = False
                mult = 1

            calcdmg = mult * ((((atklevel)/5 + 2) * 3 * (atkstat + 2) + atklevel * 2) / (defstat + 2))

            self.dmg = int(random.randint(88, 100) * calcdmg / 100)

        else :
            atkstat = max(attacker["stats"]["spa"] + attacker["weapon"]["spa"], attacker["stats"]["atk"] + attacker["weapon"]["atk"])
            defstat = min(defender["stats"]["spd"] + defender["weapon"]["spd"], defender["stats"]["def"] + defender["weapon"]["def"])

            critchance += 10

            rd = random.randint(0, 100)

            if rd <= critchance :
                self.crit = True
                mult = critdmg
            else :
                self.crit = False
                mult = 1

            calcdmg = mult * ((((atklevel)/5 + 2) * 2 * (atkstat + 2) + atklevel * 2) / (defstat + 2))

            self.dmg = int(0.65 * random.randint(60, 100) * calcdmg / 100)

        self.dmg = max(1, self.dmg)

