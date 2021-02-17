import json


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