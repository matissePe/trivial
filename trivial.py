# bot.py
import os
import random
import pages
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from discord.ext.commands import CommandNotFound
import game
from dmg import *
import math

HELP_PAGES = 3

USER_RATE_CONST1 = 267234

USER_RATE_CONST2 = 112680

USER_RATE_CONST3 = 130984


TUFFIGANG_C_ID = 783647651349659698

TUFFIGANG_R_ID = 783647539840286741

EVAN_ID = 282264924472737792

MINDELAY = 60

MAXDELAY = 90

maxoddstime = 600

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

BOT_ID = int(os.getenv('BOT_ID'))


bot = commands.Bot(command_prefix='lefevre ')
bot.remove_command('help')


users = []
nerfeduser = 0


def diffTime(id1, id2):
    return int((id2 - id1)/5000000000)

def canGain(userID, msgID, content):
    for u in users :
        if u[0] == userID :
            if content == u[2] :
                return False, 0
            else :
                d = diffTime(u[1], msgID)
                u[1] = msgID
                u[2] = content
                if d - random.randint(0,MAXDELAY - MINDELAY) > MINDELAY :
                    return True, int(min(100, 100 * d / maxoddstime))
                else :
                    return False, 0
    users.append([userID, msgID, content])
    return True, 100


@bot.event
async def on_ready():
    myActivity = discord.Game("'lefevre help' pour la liste de commandes!")
    await bot.change_presence(status=discord.Status.dnd, activity=myActivity)
    print("C'est trivial")


@bot.event
async def on_message(message: discord.Message):
    process = True
    if message.guild is None and not message.author.bot :
        if message.author.id == 143350417093296128 :
            if "resetstats" in message.content :
                idtoreset = int(message.content.split(' ')[1])
                game.resetStats(idtoreset)
            elif "giveexp" in message.content :
                uid = int(message.content.split(' ')[1])
                amount = int(message.content.split(' ')[2])
                game.giveExp(uid, amount)

            elif "giveweapon" in message.content :
                uid = int(message.content.split(' ')[1])
                wid = int(message.content.split(' ')[2])
                game.giveWeapon(uid, wid)

            elif "delay" in message.content :
                global MINDELAY
                MINDELAY = int(message.content.split(' ')[1])
                global MAXDELAY
                MAXDELAY = int(message.content.split(' ')[2])
                global maxoddstime
                maxoddstime = int(message.content.split(' ')[3])

            elif "givepve" in message.content :
                uid = int(message.content.split(' ')[1])
                game.incPveBattles(uid)


        else :
            response = "Hop hop hop, on n'envoie pas de messages privés. Si tu as une question, il faut la poser sur le forum!"
            chan = message.channel
            await chan.send(response)
            process = False

    if not message.author.bot and len(message.mentions) > 0 :
        if str(message.mentions[0].id) == str(BOT_ID) :
            response = "Debrouille-toi."
            chan = message.channel
            await chan.send(response)
        elif str(message.mentions[0].id) == str(EVAN_ID) :
            response = "J'espere que tu le ping pour une bonne raison."
            chan = message.channel
            await chan.send(response)

    if (process and not message.author.bot) :
        if message.channel.id != TUFFIGANG_C_ID :
            if len(message.content) >= 10 and 'lefevre' not in message.content  :

                    g, p = canGain(message.author.id, message.id, message.content)

                    if g :

                        if p == 100 :

                            game.giveExp(message.author.id, random.randint(60,105))
                            game.pickupRandom(message.author.id)

                        else :

                            game.giveExp(message.author.id, random.randint(30,55))

                        if random.randint(1, 100) <= p and game.amountOfPveBattles(message.author.id) < 5 :
                            game.incPveBattles(message.author.id)

                        user = game.getUserData(message.author.id)
                        sag = user["stats"]["spd"] + user["weapon"]["spd"]

                        lootchance = int(10 + 0.6 * sag)

                        if random.randint(1, 100) < lootchance :
                            game.pickupRandom(message.author.id)

                        if random.randint(1, 100) < 31 and game.amountOfPveBattles(message.author.id) < 5 :
                            game.incPveBattles(message.author.id)

                        if message.content == "fuck ecobosto" :
                            await message.channel.send("Ecobosto est la meilleure entreprise du monde. Rejoignez-nous, ayez un avenir.")
        await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    emoji = ''
    helpEmoji = False
    weapon = False
    if(reaction.emoji == '⬅'):
        emoji = 'arrow-left'
        helpEmoji = True
    elif(reaction.emoji == '➡'):
        emoji = 'arrow-right'
        helpEmoji = True
    elif reaction.emoji == '✅':
        emoji = 'v'
    elif reaction.emoji == '❌':
        emoji = 'x'
    elif reaction.emoji == '⚔':
        emoji = 'sword'
    elif reaction.emoji == '🪄':
        emoji = 'wand'
    elif reaction.emoji == '🗡':
        emoji = 'dagg'
    elif reaction.emoji == '🥦':
        emoji = 'broc'
    elif reaction.emoji == '💧':
        emoji = 'droplet'
        weapon = True
    elif reaction.emoji == '🔥':
        emoji = 'fire'
        weapon = True
    elif reaction.emoji == '⚡':
        emoji = 'zap'
        weapon = True
    elif reaction.emoji == '◀':
        emoji = 'left'
        weapon = True
    elif reaction.emoji == '▶':
        emoji = 'right'
        weapon = True
    if (reaction.count != 1 and emoji != '' and not user.bot):
        if (reaction.me):
            if helpEmoji :
                message = reaction.message
                embed = message.embeds[0]
                footer = embed.footer.text
                page_number = int(footer.split(' ')[1])




                if (emoji == 'arrow-left' and page_number > 1):
                    pages.generate_embed(page_number - 1, embed)

                elif (emoji == 'arrow-right' and page_number < HELP_PAGES) :
                    pages.generate_embed(page_number + 1, embed)
                await message.edit(embed=embed)

            else :





                if ("<@!" + str(user.id) + ">") in (reaction.message.embeds[0].description) :



                    if weapon :
                        message = reaction.message
                        embed = message.embeds[0]
                        footer = embed.footer.text
                        page_number = int(footer.split(' ')[1])

                        fi = game.fullInventory(user.id)

                        nbPages = int(1 + (- 1 + len(fi)) / 3)


                        if (emoji == 'left' and page_number > 1):
                            newembed = createWeaponEmbed(user.id, page_number - 1)
                            await message.edit(embed=newembed)

                        elif (emoji == 'right' and page_number < nbPages) :
                            newembed = createWeaponEmbed(user.id, page_number + 1)
                            await message.edit(embed=newembed)

                        else :

                            success = False

                            if emoji == 'zap' :
                                success = game.handleWeaponChange(user.id, page_number, 0)
                            elif emoji == 'fire' :
                                success = game.handleWeaponChange(user.id, page_number, 1)
                            elif emoji == 'droplet' :
                                success = game.handleWeaponChange(user.id, page_number, 2)

                            if success :
                                newembed = discord.Embed(
                                    colour = discord.Colour.purple(),
                                    title = 'Arme équipée',
                                    description = "Vous venez de changer d'arme"
                                )
                                await message.edit(embed=newembed)

                                while reaction.message.reactions != [] :
                                    for areaction in reaction.message.reactions :
                                        async for user in areaction.users():
                                            await areaction.remove(user)




                    elif emoji == 'x' :
                        await reaction.message.delete()
                    elif emoji == 'v' :


                        if reaction.count == 3 :


                            desc = reaction.message.embeds[0].description

                            firstuser = desc.split(' ')[0].split('!')[1].split('>')[0]


                            seconduser = desc.split(' ')[3].split('!')[1].split('>')[0]


                            u1 = game.getUserData(firstuser)
                            u2 = game.getUserData(seconduser)

                            if u1["stats"]["spe"] + u1["weapon"]["spe"] > u2["stats"]["spe"] + u2["weapon"]["spe"]:
                                firstturn = str(firstuser)
                                secondturn = str(seconduser)
                            else :
                                firstturn = str(seconduser)
                                secondturn = str(firstuser)

                            duser1 = await bot.fetch_user(firstuser)
                            duser2 = await bot.fetch_user(seconduser)


                            hp1 = u1["stats"]["hp"]
                            hp2 = u2["stats"]["hp"]

                            lvl1 = str(u1["stats"]["level"])
                            lvl2 = str(u2["stats"]["level"])

                            battledesc = "Le combat vient de commencer, on s'attend à voir du beau jeu de la part des 2 participants."

                            footer = "Combattants: @" + str(duser1) + " et @" + str(duser2)

                            names = duser1.name + " VS " + duser2.name

                            newembed = createEmbed(firstturn, secondturn, names, lvl1, lvl2, hp1, hp1, hp2, hp2, 10, 10, 10, 10, battledesc, footer, False)

                            await reaction.message.edit(embed = newembed)

                            while reaction.message.reactions != [] :
                                for areaction in reaction.message.reactions :
                                    async for user in areaction.users():
                                        await areaction.remove(user)

                            reacts = ["\U00002694", "\U0001FA84", "\U0001F5E1", "\U0001F966"]

                            for r in reacts :
                                await reaction.message.add_reaction(r)

                    elif ("<@!" + str(user.id) + ">") in (reaction.message.embeds[0].description.split(',')[0]) :


                        # Input du mec qui tape

                        message = reaction.message

                        embed = message.embeds[0]

                        footer = embed.footer

                        footertxt = footer.text

                        desc = embed.description

                        isPve = footertxt == "PVE"



                        firstuser = desc.split(' ')[0].split('!')[1].split('>')[0]

                        if not isPve :
                            seconduser = desc.split(' ')[4].split('!')[1].split('>')[0]

                            user1 = footer.text.split('@')[1].split('#')[0] + '#' + footer.text.split('#')[1].split(' ')[0]

                            fighter2 = game.getUserData(seconduser)

                        else :
                            seconduser = desc.split(' ')[4]

                            fighter2 = game.getEnnemyData(game.getEnnemyIDFromName(seconduser))


                        firstturn = str(firstuser)
                        secondturn = str(seconduser)

                        duser1 = await bot.fetch_user(firstuser)





                        fighter1 = game.getUserData(firstuser)


                        if isPve or str(duser1) == user1 :
                            pnumber = 1
                        else :
                            pnumber = 2


                        await reaction.remove(user)


                        hps = getHp(embed.fields[1].name)
                        manas = getMana(embed.fields[2].name)

                        if emoji == "sword" or emoji == "wand" or emoji == "dagg" :


                            valid = True

                            if emoji == "sword":
                                myDmg = dmgCalc(fighter1, fighter2, 0)
                                attacktype = "une attaque physique"
                            elif emoji == "wand":
                                if manas[2 * (pnumber - 1)] >= 3 :
                                    myDmg = dmgCalc(fighter1, fighter2, 1)
                                    manas[2 * (pnumber - 1)] -= 4
                                    attacktype = "une attaque magique"
                                else :
                                    valid = False
                            else :
                                myDmg = dmgCalc(fighter1, fighter2, 2)
                                attacktype = "un coup sournois"

                            if valid :
                                dmg = int(myDmg.dmg)
                                isCrit = myDmg.crit
                                hps[2 * (2 - pnumber)] -= dmg
                                if hps[2 * (2 - pnumber)] <= 0 :
                                    dead = True
                                else :
                                    dead= False


                                if not dead :
                                    if manas[2 * (pnumber - 1)] < manas[1 + 2 * (pnumber - 1)]:
                                        manas[2 * (pnumber - 1)] += 1

                                    lvl1 = str(fighter1["stats"]["level"])
                                    lvl2 = str(fighter2["stats"]["level"])

                                    if not isPve :

                                        battledesc = ""

                                        if isCrit :
                                            battledesc += "Coup critique! "
                                        battledesc += user.name + " inflige " + str(dmg) + " dégâts à l'aide d'" + attacktype + "!"


                                        names = embed.fields[0].name

                                        newembed = createEmbed(secondturn, firstturn, names, lvl1, lvl2, hps[0], hps[1], hps[2], hps[3], manas[0], manas[2], manas[1], manas[3], battledesc, footertxt, False)

                                        await reaction.message.edit(embed = newembed)

                                    else :


                                        # Choix de move en fonction de l'IA de l'ennemi

                                        ia = fighter2["IA"]

                                        healing = False


                                        # IA lvl 1 : Coup sournois only
                                        if ia == 1 :
                                            damage = dmgCalc(fighter2, fighter1, 2)
                                            atkdesc = "un coup sournois"




                                        # IA lvl 2 : Attaque only, move le plus puissant
                                        elif ia >= 2 :
                                            d1 = dmgCalc(fighter2, fighter1, 0)
                                            d2 = dmgCalc(fighter2, fighter1, 2)
                                            if d1.dmg > d2.dmg :
                                                damage = d1
                                                atkdesc = "une attaque physique"
                                            else :
                                                damage = d2
                                                atktype = 2
                                                atkdesc = "un coup sournois"

                                            if manas[2] >= 3 :
                                                d3 = dmgCalc(fighter2, fighter1, 1)

                                                if damage.dmg + 5 < d3.dmg :
                                                    damage = d3
                                                    manas[2] -= 4
                                                    atktype = 1
                                                    atkdesc = "une attaque magique"




                                        # IA lvl 3 : Attaque et heal, meilleur move possible
                                            if ia == 3 :
                                                if manas[2] >= 5 :
                                                    spa = fighter2["stats"]["spa"] + fighter2["weapon"]["spa"]


                                                    # si on peut se heal l'équivalent de 1,.. tours de dégâts quand on est midlife, c'est worth


                                                    if hps[2] * 2 < hps[3] and (min(hps[3], int(hps[2] + 5 + 1/10 * hps[3] + spa * hps[3]/100))) - hps[2] > dmg + 7 :
                                                        hps[2] = min(hps[3], int(hps[2] + 5 + 1/10 * hps[3] + spa * hps[3]/100))
                                                        manas[2] -= 5
                                                        manas[3] -= 1
                                                        healing = True








                                        if manas[2] < manas[3] :
                                            manas[2] += 1


                                        if not healing :
                                            dmg = damage.dmg
                                            battledesc = ""

                                            if damage.crit :
                                                battledesc += "Coup critique! "
                                                dmg = max(int(dmg * 0.7), 1)
                                            battledesc += fighter2["name"] + " inflige " + str(dmg) + " dégâts à l'aide d'" + atkdesc + "!"

                                            hps[0] -= dmg
                                        else :
                                            battledesc = fighter2["name"] + " se soigne!"


                                        if hps[0] > 0 :

                                            names = user.name + " VS " + fighter2["name"]

                                            newembed = createEmbed(firstturn, secondturn, names, lvl1, lvl2, hps[0], hps[1], hps[2], hps[3], manas[0], manas[2], manas[1], manas[3], battledesc, footertxt, True)

                                            await reaction.message.edit(embed = newembed)

                                        else :
                                            d = ""
                                            if damage.crit :
                                                d += "Coup critique! "
                                            d += str(fighter2["name"] + " a vaincu le joueur " + user.name + " avec " + str(hps[2]) + " HPs restants!")
                                            newembed = discord.Embed(
                                                colour = discord.Colour.purple(),
                                                title = 'Duel',
                                                description = d
                                            )

                                            if str(fighter2["name"]) == "Thomas" :
                                                await user.kick()

                                            await reaction.message.edit(embed = newembed)

                                            while reaction.message.reactions != [] :
                                                for areaction in reaction.message.reactions :
                                                    async for user in areaction.users():
                                                        await areaction.remove(user)

                                else :

                                    if isPve :
                                        desc = str("Le joueur " + user.name + " a vaincu le monstre " + fighter2["name"])
                                    else :
                                        desc = str("<@!" + firstturn + ">, a triomphé de <@!" + secondturn + "> avec " + str(hps[2 * (pnumber - 1)]) + " HPs restants!")

                                    newembed = discord.Embed(
                                        colour = discord.Colour.purple(),
                                        title = 'Duel',
                                        description = desc
                                    )


                                    level1 = int(fighter1["stats"]["level"])
                                    maxexp1 = (level1 ** 3 + 1) - ((level1 - 1) ** 3 + 1)


                                    level2 = int(fighter2["stats"]["level"])
                                    maxexp2 = (level2 ** 3 + 1) - ((level2 - 1) ** 3 + 1)


                                    if isPve :
                                        exptogain = fighter2["stats"]["exp"]
                                    else :
                                        exptogain = int(((level2 + 6)/(level1 + 1)) * .1 * maxexp2 + 20)

                                    for r in user.roles :
                                        if r.id == TUFFIGANG_R_ID :
                                            exptogain = int(exptogain * 1) # confused stonks


                                    game.giveExp(firstuser, exptogain)

                                    newembed.add_field(name = "Il gagne " + str(exptogain) + " points d'experience.", value = "\u200b", inline = False)

                                    if not isPve :
                                        exptolose = int(fighter2["stats"]["exp"]/2)
                                        game.halfExp(seconduser)
                                        newembed.add_field(name = "Son adversaire perd " + str(exptolose) + " points d'experience.", value = "\u200b", inline = False)

                                    await reaction.message.edit(embed = newembed)

                                    while reaction.message.reactions != [] :
                                        for areaction in reaction.message.reactions :
                                            async for user in areaction.users():
                                                await areaction.remove(user)

                        elif emoji == "broc" :
                            if manas[2 * (pnumber - 1)] >= 5 and hps[2 * (pnumber - 1)] != hps[1 + 2 * (pnumber - 1)]:
                                manas[2 * (pnumber - 1)] -= 5
                                manas[1 + 2 * (pnumber - 1)] -= 1
                                spa = fighter1["stats"]["spa"] + fighter1["weapon"]["spa"]
                                hps[2 * (pnumber - 1)] = int(min(hps[1 + 2 * (pnumber - 1)], hps[2 * (pnumber - 1)] + 5 + 1/10 * hps[1 + 2 * (pnumber - 1)] + spa * hps[1 + 2 * (pnumber - 1)]/100))
                                battledesc = user.name + " se soigne!"

                                lvl1 = str(fighter1["stats"]["level"])
                                lvl2 = str(fighter2["stats"]["level"])

                                names = embed.fields[0].name

                                if not isPve :

                                    newembed = createEmbed(secondturn, firstturn, names, lvl1, lvl2, hps[0], hps[1], hps[2], hps[3], manas[0], manas[2], manas[1], manas[3], battledesc, footertxt, False)

                                else :

                                    newembed = createEmbed(firstturn, secondturn, names, lvl1, lvl2, hps[0], hps[1], hps[2], hps[3], manas[0], manas[2], manas[1], manas[3], battledesc, footertxt, True)

                                await reaction.message.edit(embed = newembed)


                    else :
                        await reaction.remove(user)


                else :
                    await reaction.remove(user)




@bot.event
async def on_reaction_remove(reaction, user):
    emoji = ''
    if(reaction.emoji == '⬅'):
        emoji = 'arrow-left'
    if(reaction.emoji == '➡'):
        emoji = 'arrow-right'
    if (emoji != ''):
        if (reaction.me):
            message = reaction.message
            embed = message.embeds[0]
            footer = embed.footer.text
            page_number = int(footer.split(' ')[1])

            if (emoji == 'arrow-left' and page_number > 1):
                pages.generate_embed(page_number - 1, embed)

            elif (emoji == 'arrow-right' and page_number < HELP_PAGES) :
                pages.generate_embed(page_number + 1, embed)
            await message.edit(embed=embed)




@bot.command(name='help')
async def help(ctx):

    embed = discord.Embed(
        colour = discord.Colour.purple(),
        title = 'Trivial Bot help',
        description = 'Voici la liste des commandes utilisables!'
    )

    embed.set_footer(text='Page 1')

    pages.generate_embed(1, embed) #generate page 1

    msg = await ctx.send(embed=embed)

    reactions = ['\U00002b05','\U000027a1'] #:arrow-left: , :arrow-right:
    for emoji in reactions:
        await msg.add_reaction(emoji)




@bot.command(name='info')
async def info(ctx):
    embed = discord.Embed(
        colour = discord.Colour.purple(),
        title = 'Bot Sebastien Lefevre',
        description = "Bot créé le 20/05/2020 à l'aide de discord.py suite à un amphi mémorable de Sébastien Lefèvre."
    )

    await ctx.send(embed=embed)




@bot.command(name='swing')
async def swing(ctx):
    response = "Swing est la meilleure librairie graphique de tous les langages de programmation possibles et imaginables. Il s'agit d'une technlogie jeune et souple utilisée partout dans le monde!"
    await ctx.send(response)

@bot.command(name='javadoc')
async def javadoc(ctx):
    response = "Va voir la javadoc."
    await ctx.send(response)


@bot.command(name='question')
async def question(ctx):
    with open("nb.txt", "r") as f:
        number = int(f.readline())
    number += random.randint(69,420)
    with open("nb.txt", "w") as f:
        f.write(str(number))
    response = "J'ai déjà répondu " + str(number) + " fois à cette question!"
    await ctx.send(response)


@bot.command(name='forum')
async def forum(ctx):
    response = "Si vous avez une question, utilisez les forums moodle! Après tout vous n'êtes jamais là sur le chat sur les créneaux prévus ..."
    await ctx.send(response)

@bot.command(name='ant')
async def ant(ctx):
    response = "ANT c'est un super outil open source de la fondation Apache, qui permet de faire plein de commandes utiles que vous êtes incapables de taper vous-mêmes! Suffit de faire un build.xml, ça prend quoi, 1h?"
    await ctx.send(response)


@bot.command(name='travail')
async def travail(ctx):
    response = "Vous avez autant de travail qu'en temps normal. N'oubliez pas de passer votre week-end sur le TP!"
    await ctx.send(response)




def rate1(user_id: int):
    number = ((((user_id)%USER_RATE_CONST1)%169)/32)
    number = (int(20 * (number + 4.75)))/10
    return number


def rate2(user_id: int):
    number = ((((user_id)%USER_RATE_CONST2)%169)/32)
    number = (int(20 * (number + 4.75)))/10
    return number

def rate3(user_id: int):
    number = ((((user_id)%USER_RATE_CONST3)%169)/32)
    number = (int(20 * (number + 4.75)))/10
    return number

@bot.command(name='noteprojet')
async def noteprojet(ctx):
    try:
        try:
            mentionned_user = ctx.message.mentions[0].id
        except:
            mentionned_user = ctx.author.id
        finally:
            note1 = rate1(int(mentionned_user))
            note2 = rate2(int(mentionned_user))
            note3 = rate3(int(mentionned_user))



            cposs1 = ["absolument dégueulasse", "passable pour un travail de CP", "presque pas mal", "plutôt bon", "excellent", "bien mais moins que swing quand même faut pas déconner",
                      "passable de commentaire", "presque intéressant à lire", "inqualifiable parce que j'ai pas lu", "fort sympathique à ignorer"]

            cposs2 = ["plus fun à regarder qu'à lire", "drôle par moments", "une joie à noter", "très détaillé sur les points les moins importants", "une véritable déception",
                      "[insérer une remarque faite par un autre élève]", "tout simplement le dark souls du random.org"]

            cposs3 = ["bien travaillé, on a vu que tu as passé bien plus que ton week-end dessus", "inexistant, mais j'ai pas vérifié donc np", "une superbe démonstration des possibilités (oui, avec un s) de swing",
                      "politiquement correct, c'est déjà bien", "à la hauteur de mes attentes (félicitations)", "une perte de temps pour nous deux"]

            commentaire1 = cposs1[mentionned_user % 10]
            commentaire2 = cposs2[(mentionned_user * 47) % 7]
            commentaire3 = cposs3[(mentionned_user * 81) % 6]

            nbpages1 = (mentionned_user * 37) % 158 + 5
            nbpages2 = (mentionned_user * 54) % 131 + 5
            nbpages3 = (mentionned_user * 71) % 171 + 5

            avg = int (100 * (note1 + note2 + note3) / 3) / 100

            msg = str("J'octroie à <@!" + str(mentionned_user) + "> la note de " + str(avg) + "/20.0 pour le projet de programmation:"
                + "\n\n - Le cahier des charges remis était " + commentaire1 + ", et faisait " + str(nbpages1) + " pages, il mérite donc la note de " + str(note1)
                + "\n\n - Le cahier d'analyse et de conception remis était " + commentaire2 + ", et faisait " + str(nbpages2) + " pages, il mérite donc la note de " + str(note2)
                + "\n\n - Le rendu final était " + commentaire3 + ", et faisait " + str(nbpages3) + " pages, il mérite donc la note de " + str(note3)
                )



            await ctx.send(msg)
    except:
        response = 'Il y a eu un problème. Utilisez lefevre noteprojet ou lefevre noteprojet <@User>'
        await ctx.send(response)








@bot.command(name='random')
async def randomQuote(ctx):
    quotes = ["Swing est la meilleure librairie graphique de tous les langages de programmation possibles et imaginables. Il s'agit d'une technlogie jeune et souple utilisée partout dans le monde!",
              "Si vous avez une question, utilisez les forums moodle! Après tout vous n'êtes jamais là sur le chat sur les créneaux prévus ...",
              "Vous avez autant de travail qu'en temps normal. N'oubliez pas de passer votre week-end sur le TP!",
              "Va voir la javadoc",
              "J'ai déjà répondu " + str(random.randint(69,420)) + " fois à cette question!",
              "ANT c'est un super outil open source de la fondation Apache, qui permet de faire plein de commandes utiles que vous êtes incapables de taper vous-mêmes! Suffit de faire un build.xml, ça prend quoi, 1h?"
    ]
    response = random.choice(quotes)
    await ctx.send(response)



@bot.command(name='serverinfo')
async def serverinfo(ctx):
    guild = ctx.guild
    if (guild != None) :
        ts = guild.created_at
        ts = ts.strftime('%Y-%m-%d %H:%M:%S')
        print(ctx.guild)
        embed = discord.Embed(
            colour = discord.Colour.purple(),
            title = ('Server info'),
            description = guild.description
        )
        embed.set_author(name = guild.name, icon_url = str(guild.icon_url))
        embed.add_field(name='Creation date', value=str(ts), inline = False)
        embed.add_field(name='Member count', value=str(guild.member_count), inline = False)
        embed.add_field(name='Region', value=str(guild.region), inline = False)
        embed.add_field(name='Custom emoji count', value=str(len(guild.emojis)), inline = False)
        embed.add_field(name='Owner', value=str(guild.owner), inline = False)




        await ctx.send(embed=embed)







@bot.command(name='ss')
async def showstats(ctx):
    useri = ctx.message.author.id
    user = game.getUserData(useri)
    stats = user["stats"]
    w = user["weapon"]
    embed = discord.Embed(
        colour = discord.Colour.purple(),
        title = 'Vos stats',
    )
    level = stats["level"]

    hp = stats["hp"]
    atk = stats["atk"]
    de = stats["def"]
    spa = stats["spa"]
    spd = stats["spd"]
    spe = stats["spe"]

    atkbonus = str(w["atk"])
    defbonus = str(w["def"])
    spabonus = str(w["spa"])
    spdbonus = str(w["spd"])
    spebonus = str(w["spe"])

    statpoints = stats["statpoints"]

    exp = stats["exp"]
    maxexp = (level ** 3 + 1) - ((level - 1) ** 3 + 1)
    progression = int(10 * (exp / maxexp))

    bar = "█" * progression + "░" * (10 - progression)


    embed.add_field(name=('Level ' + str(level)), value=("HP " + str(hp)), inline = False)
    embed.add_field(name=('Attaque ' + str(atk) + "  [ +" + atkbonus + " ] (atk)"), value=("Defense " + str(de) + "  [ +" + defbonus + " ] (def)"), inline = False)
    embed.add_field(name=('Att. Spe ' + str(spa) + "  [ +" + spabonus + " ] (spa)"), value=("Def. Spe " + str(spd) + "  [ +" + spdbonus + " ] (spd)"), inline = False)
    embed.add_field(name=('Vitesse ' + str(spe) + "  [ +" + spebonus + " ] (spe)"), value=("Points de stats restants " + str(statpoints)), inline = False)
    embed.add_field(name=('Exp : ' + str(exp) + " / " + str(maxexp)), value=bar, inline = False)
    await ctx.send(embed = embed)



@bot.command(name='sw')
async def showweaponstats(ctx):
    useri = ctx.message.author.id
    user = game.getUserData(useri)
    weapon = user["weapon"]
    embed = discord.Embed(
        colour = discord.Colour.purple(),
        title = 'Votre arme',
    )
    nom = weapon["name"]
    atk = weapon["atk"]
    de = weapon["def"]
    spa = weapon["spa"]
    spd = weapon["spd"]
    spe = weapon["spe"]


    embed.add_field(name=('Nom : ' + nom), value="-----------", inline = False)

    embed.add_field(name=('Attaque ' + str(atk)), value=("Defense " + str(de)), inline = False)
    embed.add_field(name=('Att. Spe ' + str(spa)), value=("Def. Spe " + str(spd)), inline = False)
    embed.add_field(name=('Vitesse ' + str(spe)), value="-----------", inline = False)

    await ctx.send(embed = embed)




@bot.command(name='up')
async def usepoint(ctx, *args):
    useri = ctx.message.author.id

    try :
        stat = args[0]
        amount = 1
        try :
            amount = int(args[1])
        except :
            pass
        if stat in ["hp", "atk", "def", "spa", "spd", "spe"]:
            if game.increaseStat(useri, stat, amount) :
                if (stat == "hp") :
                    amount *= 2
                response = "La stat de " + stat + " a ete augmentée de " + str(amount)
            else :
                response = "Une erreur s'est produite en tentant d'augmenter votre stat"
        else :
            response = "Indiquez une stat valide (hp, atk, def, spa, spd, spe)"
    except Exception as e:
        response = 'lefevre usepoint <stat> [amount]'
    finally :
        await ctx.send(response)



@bot.command(name='duel')
async def duel(ctx, *args):
    embed = None
    valid = False
    try:
        mentionned_user = ctx.message.mentions[0]
        useri1 = ctx.message.author.id
        useri2 = mentionned_user.id

        if useri1 != useri2 :

            user1 = game.getUserData(useri1)
            user2 = game.getUserData(useri2)


            embed = discord.Embed(
                colour = discord.Colour.purple(),
                title = 'Duel',
                description = "Loading"
            )
            response = ""

            valid = True

        else :
            response = "Vous ne pouvez pas vous battre en duel contre vous-même!"

    except:
        response = "lefevre duel @User"
    finally:
        msg = await ctx.send(response, embed = embed)
        if valid :
            newembed = discord.Embed(
                colour = discord.Colour.purple(),
                title = 'Duel',
                description = str("<@!" + str(useri1) + "> a provoque <@!" + str(useri2) + "> en duel!")
            )

            level1 = int(user1["stats"]["level"])
            maxexp1 = (level1 ** 3 + 1) - ((level1 - 1) ** 3 + 1)


            level2 = int(user2["stats"]["level"])
            maxexp2 = (level2 ** 3 + 1) - ((level2 - 1) ** 3 + 1)

            difftropelevee = 0.8 * max(level1, level2) - min(level1, level2) - 5


            exptogain1 = int(((level2 + 6)/(level1 + 1)) * .1 * maxexp2 + 20)
            exptogain2 = int(((level1 + 6)/(level2 + 1)) * .1 * maxexp1 + 20)

            if difftropelevee > 1 :
                exptogain1 /= difftropelevee
                exptogain2 /= difftropelevee

                exptogain1 = max(20, int(exptogain1))
                exptogain2 = max(20, int(exptogain2))

            newembed.add_field(name = (ctx.message.author.name + " est niveau " + str(level1) + "."), value = "Il pourrait gagner " + str(exptogain1) +" exp!", inline = False)
            newembed.add_field(name = (mentionned_user.name + " est niveau " + str(level2) + "."), value =  "Il pourrait gagner " + str(exptogain2) +" exp!", inline = False)
            await msg.edit(embed = newembed)
            reactions = ['\U00002705','\U0000274C'] #:white_check_mark: , :x:
            for emoji in reactions:
                await msg.add_reaction(emoji)




def getHp(hpembed):
    hpembed = " ".join(hpembed.split())
    hp1 = int(hpembed.split(' ')[1])
    maxhp1 = int(hpembed.split(' ')[3])
    hp2 = int(hpembed.split(' ')[5])
    maxhp2 = int(hpembed.split(' ')[7])
    return [hp1, maxhp1, hp2, maxhp2]

def getMana(manaembed):
    manaembed = " ".join(manaembed.split())
    mana1 = int(manaembed.split(' ')[1])
    maxmana1 = int(manaembed.split(' ')[3])
    mana2 = int(manaembed.split(' ')[5])
    maxmana2 = int(manaembed.split(' ')[7])
    return [mana1, maxmana1, mana2, maxmana2]

def dmgCalc(attacker, defender, w):
    return Dmg(attacker, defender, w)

def createEmbed(firstturn, secondturn, names, lvl1, lvl2, hp1, maxhp1, hp2, maxhp2, mana1, mana2, maxmana1, maxmana2, battledesc, footer, isPve):
    if isPve :
        mydesc = str("<@!" + firstturn + ">, choisis une attaque! " + secondturn + " se défend.")
    else :
        mydesc = str("<@!" + firstturn + ">, choisis une attaque! <@!" + secondturn + "> se défend.")


    newembed = discord.Embed(
        colour = discord.Colour.purple(),
        title = 'Duel',
        description = mydesc
    )

    hpbar1 = "█" * int(10 * hp1/maxhp1) + "░" * (10 - int(10 * hp1/maxhp1))
    hpbar2 = "█" * int(10 * hp2/maxhp2) + "░" * (10 - int(10 * hp2/maxhp2))

    manabar1 = "█" * int(10 * mana1/10) + "░" * (10 - int(10 * mana1/maxmana1))
    manabar2 = "█" * int(10 * mana2/10) + "░" * (10 - int(10 * mana2/maxmana2))

    spacebetween= " " * 24
    spacebetween2= " " * 15

    newembed.add_field(name = names, value = "Lvl " + lvl1 + " VS Lvl " + lvl2)

    newembed.add_field(name =  "HP " + str(hp1) + " / " + str(maxhp1) + spacebetween + "HP " + str(hp2) + " / " + str(maxhp2), value = hpbar1 + " - - - " + hpbar2, inline = False)

    newembed.add_field(name =  "Mana " + str(mana1) + " / " + str(maxmana1) + spacebetween2 + "Mana " + str(mana2) + " / " + str(maxmana2), value = manabar1 + " - - - " + manabar2, inline = False)

    newembed.add_field(name = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - -", value = "\u200b", inline = False)

    newembed.add_field(name = ":crossed_swords: Attaque physique        :magic_wand: Attaque magique", value = "\u200b", inline = False)

    newembed.add_field(name = ":dagger: Coup sournois             :broccoli: Sort de soin", value = "\u200b", inline = False)

    newembed.add_field(name = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - -", value = "\u200b", inline = False)

    newembed.add_field(name = battledesc, value = "\u200b", inline = False)

    newembed.set_footer(text = footer)

    return newembed



@bot.command(name='pve')
async def pve(ctx, *args):
    useri1 = ctx.message.author.id
    user1 = game.getUserData(useri1)
    if (game.canPve(useri1)):

        ennemy = game.randomEnnemy(user1)

        maxhp1 = user1["stats"]["hp"]
        hp1 = maxhp1
        hp2 = ennemy["stats"]["hp"]

        if user1["stats"]["spe"] + user1["weapon"]["spe"] < ennemy["stats"]["spe"] + ennemy["weapon"]["spe"]:
            damage = dmgCalc(ennemy, user1, 2)
            dmg = max(1, int(0.5 * damage.dmg))
            battledesc = ""

            if damage.crit :
                battledesc += "Coup critique! "
            battledesc += ennemy["name"] + " inflige " + str(dmg) + " dégâts à l'aide d'un coup sournois!"

            hp1 = max(1, hp1 - dmg)

        else :
            battledesc = "Le combat vient de commencer, on souhaite bonne chance au joueur humain " + ctx.message.author.name +  "."



        firstturn = str(useri1)
        secondturn = ennemy["name"]


        lvl1 = str(user1["stats"]["level"])
        lvl2 = str(ennemy["stats"]["level"])

        footer = "PVE"

        names = ctx.message.author.name + " VS " + ennemy["name"]

        embed = createEmbed(firstturn, secondturn, names, lvl1, lvl2, hp1, maxhp1, hp2, hp2, 10, 10, 10, 10, battledesc, footer, True)

        msg = await ctx.send(embed = embed)

        reacts = ["\U00002694", "\U0001FA84", "\U0001F5E1", "\U0001F966"]

        for r in reacts :
            await msg.add_reaction(r)

    else :
        embed = discord.Embed(
            colour = discord.Colour.purple(),
            title = 'PVE',
            description = str("Vous n'avez pas d'ennemi à affronter, revenez plus tard!")
        )

        await ctx.send(embed = embed)


@bot.command(name='pveamount')
async def pveamount(ctx):
    msg = str("Vous avez " + str(game.amountOfPveBattles(ctx.message.author.id)) + " combats restants.")
    await ctx.send(msg)


def createWeaponEmbed(userID, pageNumber):
    embed = discord.Embed(
        colour = discord.Colour.purple(),
        title = 'Inventaire',
        description = str("Voici l'inventaire de <@!" + str(userID) + ">")
    )

    fields = game.retInventory(userID, pageNumber - 1)


    emojis = [":zap:", ":fire:", ":droplet:"]
    i = 0

    if fields != None :
        for f in fields :
            embed.add_field(name = f, value = "Equippez l'arme en reagissant avec " + emojis[i], inline = False)
            i += 1

    fi = game.fullInventory(userID)

    nbPages = int(1 + (- 1 + len(fi)) / 3)

    ft = str("Page " + str(pageNumber) + " / " + str(nbPages))

    embed.set_footer(text = ft)

    return embed


@bot.command(name='cw')
async def changeweapon(ctx):
    embed = createWeaponEmbed(ctx.message.author.id, 1)

    msg = await ctx.send(embed = embed)

    reacts = ["\U000025C0", "\U000026A1", "\U0001F525", "\U0001F4A7", "\U000025B6"]

    for r in reacts :
        await msg.add_reaction(r)


@bot.command(name='leaderboard')
async def leaderboard(ctx):
    embed = discord.Embed(
        colour = discord.Colour.purple(),
        title = 'Leaderboard',
        description = "Classement des joueurs les plus haut niveau"
    )

    lead = game.getBestPlayers()

    i = 1

    for u in lead :
        duser = await bot.fetch_user(u[0])
        embed.add_field(name = str(duser), value = str("#" + str(i) + " Level " + str(u[1])), inline = False)
        i += 1

    await ctx.send(embed = embed)



@bot.command(name='resetstats')
async def resetstats(ctx):
    game.resetStats(ctx.author.id)
    msg = str("Vos stats ont été réinitialisées!")
    await ctx.send(msg)




@bot.command(name='sellcurrweapon')
async def sellCurrentWeapon(ctx):
    success, exp = game.sellWeapon(ctx.author.id)
    if success :
        msg = str("Votre arme a ete vendue pour " + str(exp) + "exp!")
    else :
        msg = str("Une erreur est survenue pendant la vente de votre arme.")
    await ctx.send(msg)

bot.run(TOKEN)
