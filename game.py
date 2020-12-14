import json
import random


def retDefaultUser(userID, statpoints, level, exp):
    return {"id" : str(userID),
                "stats" : {
                    "level" : level,
                    "hp" : 5,
                    "atk" : 1,
                    "def" : 1,
                    "spa" : 1,
                    "spd" : 1,
                    "spe" : 1,
                    "statpoints": statpoints,
                    "exp" : exp
                    },
                "weapon": {
                    "id" : 0,
    				"name" : "Mains",
    				"atk" : 1,
    				"def" : 1,
    				"spa" : 0,
    				"spd" : 0,
    				"spe" : 2
			     },
			     "inventaire": [

			     ],
                 "pvebattles" : 0
                }



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
                return user

        user = retDefaultUser(userID, 10, 0, 0)
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

    if weaponId not in inventaire :
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
    totalstatpoints = user["stats"]["level"] * 5 + 10
    user = retDefaultUser(userID, totalstatpoints, user["stats"]["level"], user["stats"]["exp"])


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

    if user["pvebattles"] > 0 :
        user["pvebattles"] -= 1
        updateUser(user)
        return True
    else :
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


#resetStats(143350417093296128)