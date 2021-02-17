import json
import random
from ennemies import *
import xp

def retDefaultUser(user_id, statpoints, level, exp, wep, ppoint, pstat, pperk):
    default_user = {
        "id": str(user_id),
        "stats": {
            "level": level,
            "hp": 10,
            "atk": 5,
            "def": 5,
            "spa": 5,
            "spd": 5,
            "spe": 5,
            "statpoints": statpoints,
            "exp": exp
        },
        "weapon": wep,
        "inventaire": [
            {"id": 0}
        ],
        "pvebattles": 0,
        "sp": "None",
        "ppoints": ppoint,
        "pstats": pstat,
        "pperks": pperk
    }
    return default_user


def resetUser(user_id):
    defaultData = {
        "id": user_id,
        "stats": {
            "level": 0,
            "hp": 10,
            "atk": 5,
            "def": 5,
            "spa": 5,
            "spd": 5,
            "spe": 5,
            "statpoints": 0,
            "exp": 0
        },
        "weapon": {
            "id": 0,
            "name": "Mains",
            "atk": 1,
            "def": 1,
            "spa": 0,
            "spd": 0,
            "spe": 2
        },
        "inventaire": [
            {"id": 0}
        ],
        "pvebattles": 0
    }

    # @TODO change backup system, way too heavy on I/O files
    with open('users.json') as json_file:
        data = json.load(json_file)
        users = data["users"]

        for user in users:
            if user_id == user['id']:
                users.remove(user)
                users.append(defaultData)
                break
        write_json(data)


def write_json(data, filename='users.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def getUserData(user_id):
    user_id = str(user_id)

    with open('users.json') as json_file:
        data = json.load(json_file)
        users = data["users"]

        for user in users:
            if user_id == user['id']:
                if "sp" not in user:
                    user["sp"] = "None"
                if "ppoints" not in user:
                    user["ppoints"] = 0
                    user["pstats"] = {
                        "hp": 0,
                        "atk": 0,
                    	"def": 0,
                    	"spa": 0,
                    	"spd": 0,
                    	"spe": 0,
                        "exp": 1
                    }
                    user["pperks"] = {
                        "exp": 0,
                        "stats": 0,
                        "sp": 0
                    }
                return user
        # si user not found
        wep = {
            "id": 0,
          		"name": "Mains",
          		"atk": 1,
          		"def": 1,
          		"spa": 0,
          		"spd": 0,
          		"spe": 2
        }
        pstat = {
            "hp": 0,
            "atk": 0,
         	"def": 0,
         	"spa": 0,
            "spd": 0,
         	"spe": 0,
            "exp": 1
        }
        pperk = {
            "exp": 0,
            "stats": 0,
            "sp": 0
        }

        user = retDefaultUser(user_id, 0, 0, 0, wep, 0, pstat, pperk)
        users.append(user)
        write_json(data)
        return user


def sortFunction(value):
	return value["id"]


def updateUser(user):
    user_id = user['id']
    inventaire = sorted(user["inventaire"], key=sortFunction)

    user["inventaire"] = inventaire
    with open('users.json') as json_file:
        data = json.load(json_file)
        users = data["users"]

        for iuser in users:
            if user_id == iuser['id']:
                users.remove(iuser)
                users.append(user)
                break

        write_json(data)


def increaseStat(user_id, stat, points):
    user_id = str(user_id)
    user = getUserData(user_id)
    if user["stats"]["statpoints"] - points >= 0 and points > 0:
        if stat == "hp":
            user["stats"]["hp"] += 2 * points
            user["stats"]["statpoints"] -= 1 * points
        else:
            user["stats"][stat] += 1 * points
            user["stats"]["statpoints"] -= 1 * points
    else:
        return False

    updateUser(user)
    return True


def pickupRandom(user_id):
    user = getUserData(user_id)

    inventaire = user["inventaire"]

    level = user["stats"]["level"]
    rd = random.randint(0, 1000)
    with open('pickups.json') as pickup_file:
        loots = None
        myLoot = None
        data = json.load(pickup_file)
        for lvl in data:
            if int(lvl) <= level:
                loots = data[lvl]
        for loot in loots:
            if loot['prob'] <= rd:
                myLoot = loot["id"]
    weaponId = {"id": myLoot}

    if weaponId not in inventaire and weaponId != user["weapon"]["id"]:
        inventaire.append(weaponId)

    updateUser(user)


def changeWeapon(user_id, weaponID):
    user = getUserData(user_id)
    inventaire = user["inventaire"]
    ijsonWeapon = {"id": weaponID}
    if ijsonWeapon in inventaire:
        oldWeapon = {"id": user["weapon"]["id"]}
        inventaire.remove(ijsonWeapon)
        inventaire.append(oldWeapon)

    with open('items.json') as item_file:
        data = json.load(item_file)
        weapons = data["weapons"]
        for weapon in weapons:
            if weapon['id'] == weaponID:
                user["weapon"] = weapon
                break

        updateUser(user)


def resetStats(user_id):

    user = getUserData(user_id)
    wep = user["weapon"]
    totalstatpoints = user["stats"]["level"] * 5
    user = retDefaultUser(user_id, totalstatpoints, user["stats"]["level"],
                          user["stats"]["exp"], wep, user["ppoints"], user["pstats"], user["pperks"])
    user = updateFromPStats(user, True)
    updateUser(user)


def randomEnnemy(user):
    level = user["stats"]["level"]
    rd = random.randint(0, 1000)
    with open('ennemyprobs.json') as pickup_file:
        ennemies = None
        ennemy = None
        data = json.load(pickup_file)
        for lvl in data:
            if int(lvl) <= level:
                ennemies = data[lvl]
        for poss in ennemies:
            if poss['prob'] <= rd:
                ennemy = poss["id"]

        return getEnnemyData(ennemy)


def amountOfPveBattles(user_id):
    user = getUserData(user_id)
    return user["pvebattles"]


def canPve(user_id):
    user = getUserData(user_id)

    if user["pvebattles"] > 0 and user["stats"]["statpoints"] <= 10:
        user["pvebattles"] -= 1
        updateUser(user)
        return True
    elif user["stats"]["statpoints"] >= 10:
        return True
    else:
        return False


def incPveBattles(user_id):
    user = getUserData(user_id)
    user["pvebattles"] += 1
    updateUser(user)


def convertToNames(weaponArr):
    with open('items.json') as item_file:
        data = json.load(item_file)
        weapons = data["weapons"]

        ret = []

        for weapon in weaponArr:
            wid = weapon["id"]
            for w in weapons:
                if w["id"] == wid:
                    ret.append(w["name"])
                    break

        return ret


def retInventory(user_id, page):
    inv = fullInventory(user_id)
    if page <= (1 + (-1 + len(fullInventory(user_id))) / 3):
        return convertToNames(inv[page * 3: page * 3 + 3])
    else:
        return None


def fullInventory(user_id):
    return getUserData(user_id)["inventaire"]


def handleWeaponChange(user_id, page, index):
    page -= 1
    inv = fullInventory(user_id)[page * 3: page * 3 + 3]
    if index < len(inv):
        wid = inv[index]["id"]
        changeWeapon(user_id, wid)
        return True
    return False


def giveWeapon(user_id, newW):
    user = getUserData(user_id)

    inventaire = user["inventaire"]

    weaponId = {"id": newW}

    if weaponId not in inventaire:
        inventaire.append(weaponId)

    updateUser(user)


def getBestPlayers():
    with open('users.json') as user_file:
        data = json.load(user_file)["users"]
        levels = []
        for user in data:
            levels.append([user["id"],
                           user["stats"]["level"],
                           user["stats"]["exp"]])
        levels.sort(key=lambda lvl: (lvl[1], lvl[2]), reverse=True)
        return levels[:10]


def removeFromInventory(user_id, itemID):
    user = getUserData(user_id)

    inventaire = user["inventaire"]

    w = {
        "id": itemID
    }

    inventaire.remove(w)

    updateUser(user)


def sellWeapon(user_id):
    user = getUserData(user_id)

    try:
        weaponExp = int(user["weapon"]["exp"] * user["pstats"]["exp"])
        weaponId = user["weapon"]["id"]
        if weaponExp == 0:
            return False, 0
        else:
            changeWeapon(user_id, 0)
            removeFromInventory(user_id, weaponId)
            xp.giveExp(user_id, weaponExp)
            return True, weaponExp
    except:
        return False, 0


def getSP(spName):
    with open('sps.json') as sp_file:
        data = json.load(sp_file)["sps"]
        for s in data:
            if s["name"] == spName:
                return s


def chgSpec(user_id, spname):
    user = getUserData(user_id)
    if user["stats"]["level"] < 30:
        return False
    if user["stats"]["level"] >= 70 and user["pperks"]["sp"] > 0:
        spname += "+"
    if user["stats"]["level"] >= 120 and user["pperks"]["sp"] > 1:
        spname += "+"
    user["sp"] = spname
    updateUser(user)
    return True


def givePrestige(user_id, amount):
    user = getUserData(user_id)
    user["ppoints"] += amount
    user["stats"]["level"] = 0
    user["stats"]["exp"] = 0
    updateUser(user)
    resetStats(user_id)


def setPrestige(user_id, amount):
    user = getUserData(user_id)
    user["ppoints"] = amount
    updateUser(user)


def upPres(user_id, item, costs):
    user = getUserData(user_id)

    eCost, stCost, spCost = costs

    p = user["ppoints"]

    if item == 'sp':
        if user["pperks"]["sp"] >= 2 or p < spCost:
            return False
        else:
            user["ppoints"] -= spCost
    elif item == 'exp':
        if p < eCost:
            return False
        else:
            user["pstats"]["exp"] += 0.5
            user["ppoints"] -= eCost
    else:
        if p < stCost:
            return False
        else:
            user["pstats"]["hp"] += 10
            user["pstats"]["atk"] += 5
            user["pstats"]["def"] += 5
            user["pstats"]["spa"] += 5
            user["pstats"]["spd"] += 5
            user["pstats"]["spe"] += 5

            user = updateFromPStats(user, False)
            user["ppoints"] -= stCost

    user["pperks"][item] += 1

    updateUser(user)

    return True


def updateFromPStats(user, isReset):
    s = user["stats"]

    if isReset:
        r = user["pperks"]["stats"]
    else:
        r = 1
    s["hp"] += 10 * r
    s["atk"] += 5 * r
    s["def"] += 5 * r
    s["spa"] += 5 * r
    s["spd"] += 5 * r
    s["spe"] += 5 * r
    return user

#resetStats(143350417093296128)
#getBestPlayers()
