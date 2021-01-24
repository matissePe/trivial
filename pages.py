import discord
from discord.ext import commands

def generate_embed(page_number, embed):
    dispatcher = {1: page_1, 2: page_2, 3:page_3, 4:page_4, 5:page_5, 6:page_6, 7:page_7, 8:page_8, 9:page_9, 10:page_10}
    embed.clear_fields()
    embed.set_footer(text=str('Page ' + str(page_number)))
    run(dispatcher[page_number], embed)

def run(f, embed):
    f(embed)



def page_1(embed):
    embed.add_field(name='lefevre ant', value="ANT c'est super!", inline = False)
    embed.add_field(name='lefevre noteprojet [@User]', value="Determine votre note au projet de programmation, ou celle de l'utilisateur mentionné", inline = False)
    embed.add_field(name='lefevre swing', value='Parle de swing', inline = False)
    embed.add_field(name='lefevre forum', value='Parle du forum', inline = False)
    embed.add_field(name='lefevre travail', value='Parle de notre charge de travail', inline = False)
    embed.add_field(name='lefevre javadoc', value="C'est pas mon travail de vous faire apprendre", inline = False)
    embed.add_field(name='lefevre question', value='Déjà répondu à cette question.', inline = False)
    embed.add_field(name='lefevre random', value='( ͡° ͜ʖ ͡°)', inline = False)




def page_2(embed):
    embed.add_field(name='lefevre help', value='Affiche ce message', inline = False)
    embed.add_field(name='lefevre info', value='Affiche des informations sur le bot', inline = False)
    #embed.add_field(name='trivial rate', value='Note un utilisateur sur 10', inline = False)


def page_3(embed):
    embed.add_field(name='lefevre ss', value='Montre vos stats', inline = False)
    embed.add_field(name='lefevre sw', value='Montre les stats de votre arme', inline = False)
    embed.add_field(name='lefevre up', value='Utilisez des points pour augmentez vos stats', inline = False)
    embed.add_field(name='lefevre duel', value='Provoquez un ennemi en duel', inline = False)
    embed.add_field(name='lefevre pve', value='Faites un combat en PVE', inline = False)
    embed.add_field(name='lefevre pveamount', value='Montre vos nombres de combats en PVE restants', inline = False)
    embed.add_field(name='lefevre cw', value='Permet de changer d\'arme', inline = False)



def page_4(embed):
    embed.add_field(name='lefevre resetstats', value='Permet de reset vos stats', inline = False)
    embed.add_field(name='lefevre sellcurrweapon', value='Permet de vendre votre arme contre de l\'exp', inline = False)
    embed.add_field(name='lefevre sp', value='Montre les stats de votre spécialité', inline = False)
    embed.add_field(name='lefevre spec', value='Permet de changer de spécialité', inline = False)
    embed.add_field(name='lefevre prestige', value='Vous explique comment fonctionne le prestige', inline = False)
    embed.add_field(name='lefevre pshop', value="Vous permet d'acceder au magasin de prestige", inline = False)


def page_5(embed):
    embed.add_field(name='TEXTE p5', value='HOHOHO', inline = False)


def page_6(embed):
    embed.add_field(name='TEXTE p6', value='HOHOHO', inline = False)


def page_7(embed):
    embed.add_field(name='TEXTE p7', value='HOHOHO', inline = False)


def page_8(embed):
    embed.add_field(name='TEXTE p8', value='HOHOHO', inline = False)


def page_9(embed):
    embed.add_field(name='TEXTE p9', value='HOHOHO', inline = False)


def page_10(embed):
    embed.add_field(name='TEXTE p10', value='HOHOHO', inline = False)
