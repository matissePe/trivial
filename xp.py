import game
from discord import user


# mdr j'ai factorisé sans réfléchir je me suis rendu compte de comment
# t'as utilise ca contre nous 
def halfExp(user_id):
    user = game.getUserData(user_id)
    exp = user["stats"]["exp"]
    exp = int(exp/2)
    user["stats"]["exp"] = exp

    game.updateUser(user)

def dixPExp(user_id):
    user = game.getUserData(user_id)
    exp = user["stats"]["exp"]
    exp = int(exp * 0.9)
    user["stats"]["exp"] = exp

    game.updateUser(user)
    
    
def getPrestigeGain(user):
    lvl = user["stats"]["level"]
    gain = int(10 + (lvl - 50)**1.2)
    return gain


def calcExp(level: int, opponent: int):
    maxexp1 = (level ** 3 + 1) - ((level - 1) ** 3 + 1)
    maxexp2 = (opponent ** 3 + 1) - ((opponent - 1) ** 3 + 1)

    difftropelevee = 0.8 * max(level, opponent) - min(level, opponent) - 5

    exptogain = int(((opponent + 6)/(level + 1)) * .1 * maxexp2 + 20)
    
    if difftropelevee > 1:
        exptogain /= difftropelevee
        exptogain = max(20, int(exptogain)) # au moins 20 d'xp
    return exptogain

def giveExp(user_id, amount):
    user = game.getUserData(user_id)
    level = user["stats"]["level"]
    exp = user["stats"]["exp"]

    while amount > 0:
        maxexp = (level ** 3 + 1) - ((level - 1) ** 3 + 1)
        if amount >= maxexp - exp:
            level += 1
            amount -= (maxexp - exp)
            exp = 0
            user["stats"]["statpoints"] += 5
            if level == 70 and user["sp"] is not None and user["pperks"]["sp"] > 0:
                user["sp"] += "+"
            elif level == 120 and user["sp"] is not None and user["pperks"]["sp"] > 1:
                user["sp"] += "+"
        else:
            exp += amount
            amount = 0

    user["stats"]["level"] = level
    user["stats"]["exp"] = exp

    game.updateUser(user)