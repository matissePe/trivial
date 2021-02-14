import game
import random


class Dmg:
    def __init__(self, attacker, defender, atkmethod, hpAtk):

        atklevel = attacker["stats"]["level"]

        sp1 = game.getSP(attacker["sp"])
        sp2 = game.getSP(defender["sp"])

        atkspeed = attacker["stats"]["spe"] + \
            attacker["weapon"]["spe"] + sp1["stats"]["spe"]

        atkatk = attacker["stats"]["atk"] + \
            attacker["weapon"]["atk"] + sp1["stats"]["atk"]

        if sp1["name"] == "Berserker":
            atkatk += int(0.5 * ((attacker["stats"]
                                  ["hp"] + sp1["stats"]["hp"]) - hpAtk))
        elif sp1["name"] == "Berserker+":
            atkatk += int(0.6 * ((attacker["stats"]
                                  ["hp"] + sp1["stats"]["hp"]) - hpAtk))
        elif sp1["name"] == "Berserker++":
            atkatk += int(0.7 * ((attacker["stats"]
                                  ["hp"] + sp1["stats"]["hp"]) - hpAtk))

        atkspa = attacker["stats"]["spa"] + \
            attacker["weapon"]["spa"] + sp1["stats"]["spa"]

        if sp1["name"] == "Bloodmage":
            atkspa += int(0.5 * ((attacker["stats"]
                                  ["hp"] + sp1["stats"]["hp"]) - hpAtk))
        elif sp1["name"] == "Bloodmage+":
            atkspa += int(0.6 * ((attacker["stats"]
                                  ["hp"] + sp1["stats"]["hp"]) - hpAtk))
        elif sp1["name"] == "Bloodmage++":
            atkspa += int(0.7 * ((attacker["stats"]
                                  ["hp"] + sp1["stats"]["hp"]) - hpAtk))

        defdef = defender["stats"]["def"] + \
            defender["weapon"]["def"] + sp2["stats"]["def"]

        defspd = defender["stats"]["spd"] + \
            defender["weapon"]["spd"] + sp2["stats"]["spd"]

        critchance = 5 + atkspeed - defspd

        critdmg = max(2, 2 + 0.01 * (atkatk - defdef))

        if "Battlemage" in sp1["name"]:
            atkatk += atkspa
            atkspa = atkatk

        if sp1["name"] == "Battlemage+":
            atkatk = atkatk * 1.2
            atkspa = atkatk

        elif sp1["name"] == "Battlemage++":
            atkatk = atkatk * 1.4
            atkspa = atkatk

        if atkmethod == 0:
            atkstat = atkatk
            defstat = defdef

            rd = random.randint(0, 100)

            if rd <= critchance:
                self.crit = True
                mult = critdmg

                if sp1["name"] == "Assassin":
                    defstat = int(max(1, 0.8 * defstat))
                elif sp1["name"] == "Assassin+":
                    defstat = int(max(1, 0.7 * defstat))
                elif sp1["name"] == "Assassin++":
                    defstat = int(max(1, 0.6 * defstat))

            else:
                self.crit = False
                mult = 1

            calcdmg = mult * ((((atklevel)/5 + 2) * 2 *
                               (atkstat + 2) + atklevel * 2) / (defstat + 2))

            self.dmg = int(random.randint(88, 100) * calcdmg / 100)

        elif atkmethod == 1:
            atkstat = atkspa
            defstat = defspd

            rd = random.randint(0, 100)

            if rd <= critchance:
                self.crit = True
                mult = critdmg
            else:
                self.crit = False
                mult = 1

                if sp1["name"] == "Assassin":
                    defstat = int(max(1, 0.8 * defstat))
                elif sp1["name"] == "Assassin+":
                    defstat = int(max(1, 0.7 * defstat))
                elif sp1["name"] == "Assassin++":
                    defstat = int(max(1, 0.6 * defstat))

            calcdmg = mult * ((((atklevel)/5 + 2) * 3 *
                               (atkstat + 2) + atklevel * 2) / (defstat + 2))

            self.dmg = int(random.randint(88, 100) * calcdmg / 100)

        else:
            atkstat = max(atkatk, atkspa)
            defstat = min(defdef, defspd)

            critchance += 10

            rd = random.randint(0, 100)

            if rd <= critchance:
                self.crit = True
                mult = critdmg
            else:
                self.crit = False
                mult = 1

                if sp1["name"] == "Assassin":
                    defstat = int(max(1, 0.8 * defstat))
                elif sp1["name"] == "Assassin+":
                    defstat = int(max(1, 0.7 * defstat))
                elif sp1["name"] == "Assassin++":
                    defstat = int(max(1, 0.6 * defstat))

            calcdmg = mult * ((((atklevel)/5 + 2) * 2 * (atkstat + 2) + atklevel * 2) / (defstat + 2))
            self.dmg = int(0.65 * random.randint(60, 100) * calcdmg / 100)
        self.dmg = max(1, self.dmg)
