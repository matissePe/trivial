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