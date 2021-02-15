import json
import random

def retDefaultUser(userID, statpoints, level, exp, wep, ppoint, pstat, pperk):
    return {"id" : str(userID),
                "stats" : {
                    "level" : level,
                    "hp" : 10,
                    "atk" : 5,
                    "def" : 5,
                    "spa" : 5,
                    "spd" : 5,
                    "spe" : 5,
                    "statpoints": statpoints,
                    "exp" : exp
                },
                "weapon": wep,
			    "inventaire": [
                    {"id" : 0}
			    ],
                 "pvebattles" : 0,
                 "sp" : "None",
                 "ppoints" : ppoint,
                 "pstats" : pstat,
                 "pperks" : pperk
                }


def resetUser(userID):
    defaultData = {
        "id": userID,
        "stats": {
            "level": 0,
            "hp": 5,
            "atk": 1,
            "def": 1,
            "spa": 1,
            "spd": 1,
            "spe": 1,
            "statpoints": 10,
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
            {"id" : 0}
	    ],
        "pvebattles": 0
    }
    
    with open('users.json') as json_file:
        data = json.load(json_file)
        users = data["users"]
        
        for iuser in users:
            if userID == iuser['id']:
                users.remove(iuser)
                users.append(defaultData)
                break
        write_json(data)
    
    

def write_json(data, filename='users.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

def getUserData(userID):
    userID = str(userID)

    with open('users.json') as json_file:
        data = json.load(json_file)
        users = data["users"]

        for user in users :
            if userID == user['id']:
                if "sp" not in user :
                    user["sp"] = "None"
                if "ppoints" not in user :
                    user["ppoints"] = 0
                    user["pstats"] = {
                        "hp"  : 0,
                        "atk" : 0,
        				"def" : 0,
        				"spa" : 0,
        				"spd" : 0,
        				"spe" : 0,
                        "exp" : 1
                    }
                    user["pperks"] = {
                        "exp" : 0,
                        "stats" : 0,
                        "sp" : 0
                    }
                return user

        # si user not found

        wep = {
            "id" : 0,
    		"name" : "Mains",
    		"atk" : 1,
    		"def" : 1,
    		"spa" : 0,
    		"spd" : 0,
    		"spe" : 2
		}

        pstat = {
            "hp"  : 0,
            "atk" : 0,
			"def" : 0,
			"spa" : 0,
            "spd" : 0,
			"spe" : 0,
            "exp" : 1
        }
        
        pperk = {
            "exp" : 0,
            "stats" : 0,
            "sp" : 0
        }


        user = retDefaultUser(userID, 0, 0, 0, wep, 0, pstat, pperk)
        users.append(user)
        write_json(data)
        return user

def sortFunction(value):
	return value["id"]

def updateUser(user):
    userID = user['id']
    inventaire = sorted(user["inventaire"], key=sortFunction)

    user["inventaire"] = inventaire
    with open('users.json') as json_file:
        data = json.load(json_file)
        users = data["users"]

        for iuser in users :
            if userID == iuser['id']:
                users.remove(iuser)
                users.append(user)
                break

        write_json(data)


def increaseStat(userID, stat, points):
    userID = str(userID)
    user = getUserData(userID)
    if user["stats"]["statpoints"] - points >= 0 and points > 0 :
        if stat == "hp" :
            user["stats"]["hp"] += 2 * points
            user["stats"]["statpoints"] -= 1 * points
        else :
            user["stats"][stat] += 1 * points
            user["stats"]["statpoints"] -= 1 * points
    else :
        return False

    updateUser(user)
    return True


def pickupRandom(userID):
    user = getUserData(userID)

    inventaire = user["inventaire"]

    level = user["stats"]["level"]
    rd = random.randint(0, 1000)
    with open('pickups.json') as pickup_file:
        loots = None
        myLoot = None
        data = json.load(pickup_file)
        for lvl in data:
            if int(lvl) <= level :
                loots = data[lvl]
        for loot in loots :
            if loot['prob'] <= rd :
                myLoot = loot["id"]
    weaponId = {"id" : myLoot}

    if weaponId not in inventaire and weaponId != user["weapon"]["id"] :
        inventaire.append(weaponId)

    updateUser(user)


def changeWeapon(userID, weaponID):
    user = getUserData(userID)
    inventaire = user["inventaire"]
    ijsonWeapon = {"id" : weaponID}
    if ijsonWeapon in inventaire :
        oldWeapon = {"id" : user["weapon"]["id"]}
        inventaire.remove(ijsonWeapon)
        inventaire.append(oldWeapon)

    with open('items.json') as item_file:
        data = json.load(item_file)
        weapons = data["weapons"]
        for weapon in weapons :
            if weapon['id'] == weaponID :
                user["weapon"] = weapon
                break

        updateUser(user)


def resetStats(userID):

    user = getUserData(userID)
    wep = user["weapon"]
    totalstatpoints = user["stats"]["level"] * 5
    user = retDefaultUser(userID, totalstatpoints, user["stats"]["level"], user["stats"]["exp"], wep, user["ppoints"], user["pstats"], user["pperks"])
    user = updateFromPStats(user, True)
    updateUser(user)


def giveExp(userID, amount):

    user = getUserData(userID)

    level = user["stats"]["level"]

    exp = user["stats"]["exp"]

    while amount > 0 :
        maxexp = (level ** 3 + 1) - ((level - 1) ** 3 + 1)


        if amount >= maxexp - exp :
            level += 1
            amount -= (maxexp - exp)
            exp = 0
            user["stats"]["statpoints"] += 5
            if level == 70 and user["sp"] is not None and user["pperks"]["sp"] > 0 :
                user["sp"] += "+"
            elif level == 120 and user["sp"] is not None and user["pperks"]["sp"] > 1 :
                user["sp"] += "+"
        else :
            exp += amount
            amount = 0

    user["stats"]["level"] = level
    user["stats"]["exp"] = exp

    updateUser(user)


def halfExp(userID):
    user = getUserData(userID)

    exp = user["stats"]["exp"]

    exp = int(exp/2)

    user["stats"]["exp"] = exp

    updateUser(user)


def dixPExp(userID):
    user = getUserData(userID)

    exp = user["stats"]["exp"]

    exp = int(exp * 0.9)

    user["stats"]["exp"] = exp

    updateUser(user)


def getEnnemyIDFromName(ennemyName):
    with open('ennemies.json') as ennemy_file:
        data = json.load(ennemy_file)["ennemies"]

        for ennemy in data :
            if ennemy["name"] == ennemyName :
                return ennemy["id"]


def getEnnemyData(ennemy):
    ennemy = int(ennemy)
    with open('ennemies.json') as ennemy_file:
        data = json.load(ennemy_file)["ennemies"]
        for e in data :
            if int(e["id"]) == ennemy :
                return e


def randomEnnemy(user):
    level = user["stats"]["level"]
    rd = random.randint(0, 1000)
    with open('ennemyprobs.json') as pickup_file:
        ennemies = None
        ennemy = None
        data = json.load(pickup_file)
        for lvl in data:
            if int(lvl) <= level :
                ennemies = data[lvl]
        for poss in ennemies :
            if poss['prob'] <= rd :
                ennemy = poss["id"]

        return getEnnemyData(ennemy)


def amountOfPveBattles(userID):
    user = getUserData(userID)
    return user["pvebattles"]


def canPve(userID):
    user = getUserData(userID)

    if user["pvebattles"] > 0 and user["stats"]["statpoints"] <= 10:
        user["pvebattles"] -= 1
        updateUser(user)
        return True
    elif user["stats"]["statpoints"] >= 10:
        return True
    else:
        return False


def incPveBattles(userID):
    user = getUserData(userID)
    user["pvebattles"] += 1
    updateUser(user)


def convertToNames(weaponArr):
    with open('items.json') as item_file:
        data = json.load(item_file)
        weapons = data["weapons"]

        ret = []

        for weapon in weaponArr :
            wid = weapon["id"]
            for w in weapons :
                if w["id"] == wid :
                    ret.append(w["name"])
                    break

        return ret


def retInventory(userID, page):
    inv = fullInventory(userID)
    if page <= (1 + (-1 + len(fullInventory(userID))) / 3) :
        return convertToNames(inv[page * 3 : page * 3 + 3])
    else :
        return None

def fullInventory(userID) :
    return getUserData(userID)["inventaire"]


def handleWeaponChange(userID, page, index):
    page -= 1
    inv = fullInventory(userID)[page * 3 : page * 3 + 3]
    if index < len(inv) :
        wid = inv[index]["id"]
        changeWeapon(userID, wid)
        return True
    return False


def giveWeapon(userID, newW):
    user = getUserData(userID)

    inventaire = user["inventaire"]

    weaponId = {"id" : newW}

    if weaponId not in inventaire :
        inventaire.append(weaponId)

    updateUser(user)


def getBestPlayers():
    with open('users.json') as user_file:
        data = json.load(user_file)["users"]
        levels = []
        for user in data :
            levels.append([user["id"], 
                           user["stats"]["level"],
                           user["stats"]["exp"]])
        levels.sort(key = lambda lvl: (lvl[1], lvl[2]), reverse = True)
        return levels[:10]


def removeFromInventory(userID, itemID):
    user = getUserData(userID)

    inventaire = user["inventaire"]

    w = {"id" : itemID}

    inventaire.remove(w)

    updateUser(user)


def sellWeapon(userID):
    user = getUserData(userID)

    try :
        weaponExp = int(user["weapon"]["exp"] * user["pstats"]["exp"])
        weaponId = user["weapon"]["id"]
        if weaponExp == 0 :
            return False, 0
        else :
            changeWeapon(userID, 0)
            removeFromInventory(userID, weaponId)
            giveExp(userID, weaponExp)
            return True, weaponExp
    except :
        return False, 0


def getSP(spName):
    with open('sps.json') as sp_file:
        data = json.load(sp_file)["sps"]
        for s in data :
            if s["name"] == spName :
                return s


def chgSpec(userID, spname):
    user = getUserData(userID)
    if user["stats"]["level"] < 30 :
        return False
    if user["stats"]["level"] >= 70 and user["pperks"]["sp"] > 0:
        spname += "+"
    if user["stats"]["level"] >= 120 and user["pperks"]["sp"] > 1:
        spname += "+"
    user["sp"] = spname
    updateUser(user)
    return True


def givePrestige(userID, amount):
    user = getUserData(userID)
    user["ppoints"] += amount
    user["stats"]["level"] = 0
    user["stats"]["exp"] = 0
    updateUser(user)
    resetStats(userID)

def setPrestige(userID, amount):
    user = getUserData(userID)
    user["ppoints"] = amount
    updateUser(user)

def upPres(userID, item, costs):
    user = getUserData(userID)

    eCost, stCost, spCost = costs

    p = user["ppoints"]

    if item == 'sp' :
        if user["pperks"]["sp"] >= 2 or p < spCost:
            return False
        else :
            user["ppoints"] -= spCost
    elif item == 'exp' :
        if p < eCost :
            return False
        else :
            user["pstats"]["exp"] += 0.5
            user["ppoints"] -= eCost
    else :
        if p < stCost :
            return False
        else :
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

    if isReset :
        r = user["pperks"]["stats"]
    else :
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
