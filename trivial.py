# bot.py
import math
import os
import random
from datetime import datetime

import discord
from discord import Intents
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

from ennemies import *
from embed import createWeaponEmbed, createEmbed, makeSPEmbed
from utils import *
import game
import pages
from xp import getPrestigeGain, calcExp, giveExp
from dmg import *

intents = Intents.default()
intents.members = True
intents.presences = True


HELP_PAGES = 4

USER_RATE_CONST1 = 267234

USER_RATE_CONST2 = 112680

USER_RATE_CONST3 = 130984

TUFFIGANG_C_ID = 783647651349659698

TUFFIGANG_R_ID = 783647539840286741
D1A_ID         = 750451627403640974


MAIWEN_ID  = 688075252281901084
GILDAS_ID  = 158571429183356937
EVAN_ID    = 282264924472737792
ANTOINE_ID = 319444688694280192
GABRIEL_ID = 135321090699427840 #C'est moi le plus vieux sur discord hehe

INSULTES_ACTIVATED = True

MINDELAY = 60

MAXDELAY = 90

maxoddstime = 600

MAX_SP_TIER = 2

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_ID = int(os.getenv('BOT_ID'))


bot = commands.Bot(command_prefix='lefevre ', intents=intents)
bot.remove_command('help')


users = []
nerfeduser = 0


def diffTime(id1, id2):
    return int((id2 - id1)/5000000000)


def canGain(userID, msgID, content):
    for u in users:
        if u[0] == userID:
            if content == u[2]:
                return False, 0
            else:
                d = diffTime(u[1], msgID)
                u[1] = msgID
                u[2] = content
                if d - random.randint(0, MAXDELAY - MINDELAY) > MINDELAY:
                    return True, int(min(100, 100 * d / maxoddstime))
                else:
                    return False, 0
    users.append([userID, msgID, content])
    return True, 100


@bot.event
async def on_ready():
    myActivity = discord.Game("'lefevre help' pour la liste de commandes!")
    await bot.change_presence(status=discord.Status.dnd, activity=myActivity)
    insulte_tuffigang.start()
    print("C'est trivial")


@bot.event
async def on_message(message: discord.Message):
    process = True
    if message.guild is None and not message.author.bot:
        if message.author.id == 143350417093296128 or message.author.id == GABRIEL_ID:
            if "resetstats" in message.content:
                idtoreset = int(message.content.split(' ')[1])
                game.resetStats(idtoreset)
            elif "giveexp" in message.content:
                uid = int(message.content.split(' ')[1])
                amount = int(message.content.split(' ')[2])
                giveExp(uid, amount)

            elif "giveweapon" in message.content:
                uid = int(message.content.split(' ')[1])
                wid = int(message.content.split(' ')[2])
                game.giveWeapon(uid, wid)

            elif "delay" in message.content:
                global MINDELAY
                MINDELAY = int(message.content.split(' ')[1])
                global MAXDELAY
                MAXDELAY = int(message.content.split(' ')[2])
                global maxoddstime
                maxoddstime = int(message.content.split(' ')[3])

            elif "givepve" in message.content:
                uid = int(message.content.split(' ')[1])
                game.incPveBattles(uid)
        else:
            response = "Hop hop hop, on n'envoie pas de messages privés. Si tu as une question, il faut la poser sur le forum!"
            chan = message.channel
            await chan.send(response)
            process = False

    elif not message.author.bot and len(message.mentions) > 0:
        if BOT_ID in [m.id for m in message.mentions]:
            response = "Debrouille-toi."
            if message.author.id == GABRIEL_ID:
                response = "^ Cet homme a raison"
            chan = message.channel
            await chan.send(response)
            
        elif (EVAN_ID in [m.id for m in message.mentions] or GILDAS_ID in [m.id for m in message.mentions]) and message.reference is None:
            response = "J'espere que tu le ping pour une bonne raison."
            chan = message.channel
            await chan.send(response)
            
        elif message.mentions[0].id == MAIWEN_ID and message.reference is None and D1A_ID in [y.id for y in message.author.roles]:
            try:
                bot.delete_message(message)
            except:
                pass
            finally:
                response = "ntm"
                await message.channel.send(response)
    elif not message.author.bot:
        if ('🆗' in message.content or '🆒' in message.content) and D1A_ID in [y.id for y in message.author.roles]:
            await message.channel.send("pas sympa ca khey")
    
    if (process and not message.author.bot):
        if message.channel.id != TUFFIGANG_C_ID:
            if len(message.content) >= 10 and 'lefevre' not in message.content:
                g, p = canGain(message.author.id, message.id, message.content)
                if g:
                    if p == 100:
                        giveExp(message.author.id, random.randint(60, 105))
                        game.pickupRandom(message.author.id)

                    else:
                        giveExp(message.author.id, random.randint(30, 55))

                    if random.randint(1, 100) <= p and game.amountOfPveBattles(message.author.id) < 5:
                        game.incPveBattles(message.author.id)

                        user = game.getUserData(message.author.id)
                        sag = user["stats"]["spd"] + user["weapon"]["spd"] + \
                            game.getSP(user["sp"])["stats"]["spd"]

                        lootchance = int(10 + 0.6 * sag)

                    if random.randint(1, 100) < lootchance:
                        game.pickupRandom(message.author.id)

                    if random.randint(1, 100) < 31 and game.amountOfPveBattles(message.author.id) < 5:
                        game.incPveBattles(message.author.id)

                    if message.content == "fuck ecobosto":
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
        if reaction.me:
            if helpEmoji:
                message = reaction.message
                embed = message.embeds[0]
                footer = embed.footer.text
                page_number = int(footer.split(' ')[1])

                if (emoji == 'arrow-left' and page_number > 1):
                    pages.generate_embed(page_number - 1, embed)

                elif (emoji == 'arrow-right' and page_number < HELP_PAGES):
                    pages.generate_embed(page_number + 1, embed)
                await message.edit(embed=embed)
            else:
                if ("<@!" + str(user.id) + ">") in (reaction.message.embeds[0].description):

                    if weapon:
                        message = reaction.message
                        embed = message.embeds[0]
                        footer = embed.footer.text
                        page_number = int(footer.split(' ')[1])

                        fi = game.fullInventory(user.id)

                        nbPages = int(1 + (- 1 + len(fi)) / 3)

                        if (emoji == 'left' and page_number > 1):
                            newembed = createWeaponEmbed(
                                user.id, page_number - 1)
                            await message.edit(embed=newembed)

                        elif (emoji == 'right' and page_number < nbPages):
                            newembed = createWeaponEmbed(
                                user.id, page_number + 1)
                            await message.edit(embed=newembed)

                        else:

                            success = False

                            if emoji == 'zap':
                                success = game.handleWeaponChange(
                                    user.id, page_number, 0)
                            elif emoji == 'fire':
                                success = game.handleWeaponChange(
                                    user.id, page_number, 1)
                            elif emoji == 'droplet':
                                success = game.handleWeaponChange(
                                    user.id, page_number, 2)

                            if success:
                                newembed = discord.Embed(
                                    colour=discord.Colour.purple(),
                                    title='Arme équipée',
                                    description="Vous venez de changer d'arme"
                                )
                                await message.edit(embed=newembed)

                                while reaction.message.reactions != []:
                                    for areaction in reaction.message.reactions:
                                        async for user in areaction.users():
                                            await areaction.remove(user)

                    elif emoji == 'x':
                        await reaction.message.delete()
                    elif emoji == 'v':

                        if reaction.count == 3:

                            desc = reaction.message.embeds[0].description

                            firstuser = desc.split(' ')[0].split('!')[
                                1].split('>')[0]

                            seconduser = desc.split(' ')[3].split('!')[
                                1].split('>')[0]

                            u1 = game.getUserData(firstuser)
                            u2 = game.getUserData(seconduser)

                            if u1["stats"]["spe"] + u1["weapon"]["spe"] > u2["stats"]["spe"] + u2["weapon"]["spe"]:
                                firstturn = str(firstuser)
                                secondturn = str(seconduser)
                            else:
                                firstturn = str(seconduser)
                                secondturn = str(firstuser)

                            duser1 = await bot.fetch_user(firstuser)
                            duser2 = await bot.fetch_user(seconduser)

                            hp1 = u1["stats"]["hp"]
                            hp2 = u2["stats"]["hp"]

                            lvl1 = str(u1["stats"]["level"])
                            lvl2 = str(u2["stats"]["level"])

                            battledesc = "Le combat vient de commencer, on s'attend à voir du beau jeu de la part des 2 participants."

                            footer = "Combattants: @" + \
                                str(duser1) + " et @" + str(duser2)

                            names = duser1.name + " VS " + duser2.name

                            newembed = createEmbed(firstturn, secondturn, names, lvl1, lvl2, hp1,
                                                   hp1, hp2, hp2, 10, 10, 10, 10, battledesc, footer, False, 0, 0)

                            await reaction.message.edit(embed=newembed)

                            while reaction.message.reactions != []:
                                for areaction in reaction.message.reactions:
                                    async for user in areaction.users():
                                        await areaction.remove(user)

                            reacts = ["\U00002694", "\U0001FA84",
                                      "\U0001F5E1", "\U0001F966"]

                            for r in reacts:
                                await reaction.message.add_reaction(r)

                    elif ("<@!" + str(user.id) + ">") in (reaction.message.embeds[0].description.split(',')[0]):

                        # Input du mec qui tape

                        message = reaction.message

                        embed = message.embeds[0]

                        footer = embed.footer

                        footertxt = footer.text

                        desc = embed.description

                        isPve = footertxt == "PVE"

                        firstuser = desc.split(' ')[0].split('!')[1].split('>')[0]

                        if not isPve:
                            seconduser = desc.split(' ')[4].split('!')[
                                1].split('>')[0]

                            user1 = footer.text.split(
                                '@')[1].split('#')[0] + '#' + footer.text.split('#')[1].split(' ')[0]

                            fighter2 = game.getUserData(seconduser)

                        else:
                            seconduser = desc.split(' ')[4]

                            fighter2 = getEnnemyData(getEnnemyIDFromName(seconduser))

                        firstturn = str(firstuser)
                        secondturn = str(seconduser)

                        duser1 = await bot.fetch_user(firstuser)

                        fighter1 = game.getUserData(firstuser)

                        if isPve or str(duser1) == user1:
                            pnumber = 1
                        else:
                            pnumber = 2

                        await reaction.remove(user)

                        hps = getHp(embed.fields[1].name, embed.fields[2].name)

                        p1Psn = int(embed.fields[1].name.split(
                            '[')[1].split(']')[0])

                        p2Psn = int(embed.fields[2].name.split(
                            '[')[1].split(']')[0])

                        manas = getMana(
                            embed.fields[4].name, embed.fields[5].name)

                        if emoji == "sword" or emoji == "wand" or emoji == "dagg":

                            valid = True

                            vmpHeal = False

                            addPoison = False

                            if emoji == "sword":
                                myDmg = dmgCalc(
                                    fighter1, fighter2, 0, hps[2 * (pnumber - 1)])
                                attacktype = "une attaque physique"
                                if "Vampire" in fighter1["sp"]:
                                    vmpHeal = True

                            elif emoji == "wand":
                                if manas[2 * (pnumber - 1)] >= 3 or (manas[2 * (pnumber - 1)] >= 2 and "Sorcier" in fighter1["sp"]):
                                    myDmg = dmgCalc(
                                        fighter1, fighter2, 1, hps[2 * (pnumber - 1)])
                                    manas[2 * (pnumber - 1)] -= 4

                                    if fighter1["sp"] == "Sorcier":
                                        manas[2 * (pnumber - 1)] += 1
                                    elif fighter1["sp"] == "Sorcier+":
                                        manas[2 * (pnumber - 1)] += 2
                                    elif fighter1["sp"] == "Sorcier++":
                                        manas[2 * (pnumber - 1)] += 3
                                    elif "Alchimiste" in fighter1["sp"]:
                                        if pnumber == 1:
                                            p2Psn += 1
                                        else:
                                            p1Psn += 1

                                    attacktype = "une attaque magique"

                                else:
                                    valid = False

                            else:
                                myDmg = dmgCalc(
                                    fighter1, fighter2, 2, hps[2 * (pnumber - 1)])
                                attacktype = "un coup sournois"

                            if valid:
                                dmg = int(myDmg.dmg)
                                isCrit = myDmg.crit
                                hps[2 * (2 - pnumber)] -= dmg

                                if vmpHeal:
                                    if fighter1["sp"] == "Vampire++":
                                        hps[2 * (pnumber - 1)] = min(hps[2 * (pnumber - 1) + 1],
                                                                     int(hps[2 * (pnumber - 1)] + 0.8 * dmg))
                                    elif fighter1["sp"] == "Vampire+":
                                        hps[2 * (pnumber - 1)] = min(hps[2 * (pnumber - 1) + 1],
                                                                     int(hps[2 * (pnumber - 1)] + 0.65 * dmg))
                                    else:
                                        hps[2 * (pnumber - 1)] = min(hps[2 * (pnumber - 1) + 1],
                                                                     int(hps[2 * (pnumber - 1)] + 0.5 * dmg))

                                battledesc = ""
                                if isCrit:
                                    battledesc += "Coup critique! "
                                battledesc += user.name + " inflige " + \
                                    str(dmg) + " dégâts à l'aide d'" + \
                                attacktype + "!"

                                psnDmg = 0

                                if p1Psn > 0 and pnumber == 2 or p2Psn > 0 and pnumber == 1:
                                    if not isPve:
                                        if pnumber == 1:
                                            pPsn = p2Psn
                                            username = await bot.fetch_user(seconduser).name
                                        else:
                                            pPsn = p1Psn
                                            username = await bot.fetch_user(firstuser).name
                                    else:
                                        username = fighter2["name"]
                                        pPsn = p2Psn

                                    if fighter1["sp"] == "Alchimiste++":
                                        psnDmg = int(
                                            hps[1 + 2 * (2 - pnumber)] * 8 * pPsn / 100)
                                    elif fighter1["sp"] == "Alchimiste+":
                                        psnDmg = int(
                                            hps[1 + 2 * (2 - pnumber)] * 6.5 * pPsn / 100)
                                    else:
                                        psnDmg = int(
                                            hps[1 + 2 * (2 - pnumber)] * 5 * pPsn / 100)

                                    battledesc += username + " subit " + \
                                        str(psnDmg) + " dégâts de poison!"
                                    hps[2 * (2 - pnumber)] -= psnDmg

                                if hps[2 * (2 - pnumber)] <= 0:
                                    dead = True
                                else:
                                    dead = False

                                if not dead:
                                    if manas[2 * (pnumber - 1)] < manas[1 + 2 * (pnumber - 1)]:
                                        manas[2 * (pnumber - 1)] += 1

                                    lvl1 = str(fighter1["stats"]["level"])
                                    lvl2 = str(fighter2["stats"]["level"])

                                    if not isPve:

                                        names = embed.fields[0].name

                                        newembed = createEmbed(secondturn, firstturn, names, lvl1, lvl2, hps[0], hps[1], hps[2], hps[
                                                               3], manas[0], manas[2], manas[1], manas[3], battledesc, footertxt, False, p1Psn, p2Psn)

                                        await reaction.message.edit(embed=newembed)

                                    else:
                                        manacost = 0
                                        # Choix de move en fonction de l'IA de l'ennemi
                                        ia = fighter2["IA"]
                                        healing = False
                                        vmpHeal = False
                                        # IA lvl 1 : Coup sournois only
                                        if ia == 1:
                                            damage = dmgCalc(
                                                fighter2, fighter1, 2, hps[2])
                                            atkdesc = "un coup sournois"
                                            atktype = 2
                                        # IA lvl 2 : Attaque only, move le plus puissant
                                        elif ia >= 2:
                                            d1 = dmgCalc(
                                                fighter2, fighter1, 0, hps[2])
                                            d2 = dmgCalc(
                                                fighter2, fighter1, 2, hps[2])
                                            if d1.dmg > d2.dmg:
                                                damage = d1
                                                atktype = 0
                                                atkdesc = "une attaque physique"

                                                if fighter2["sp"] == "Vampire":
                                                    vmpHeal = True
                                            else:
                                                damage = d2
                                                atktype = 2
                                                atkdesc = "un coup sournois"

                                            if manas[2] >= 3 or (manas[2] >= 2 and "Sorcier" in fighter2["sp"]):
                                                d3 = dmgCalc(
                                                    fighter2, fighter1, 1, hps[2])

                                                if damage.dmg + 5 < d3.dmg:
                                                    damage = d3
                                                    manacost = 4
                                                    if fighter2["sp"] == "Sorcier":
                                                        manacost -= 1
                                                    elif fighter2["sp"] == "Sorcier+":
                                                        manacost -= 2
                                                    elif fighter2["sp"] == "Sorcier++":
                                                        manacost -= 3
                                                    atktype = 1
                                                    atkdesc = "une attaque magique"

                                        # IA lvl 3 : Attaque et heal, meilleur move possible
                                            if ia == 3:
                                                if manas[2] >= 5 or (manas[2] >= 4 and "Sorcier" in fighter2["sp"]):
                                                    spa = fighter2["stats"]["spa"] + fighter2["weapon"]["spa"] + game.getSP(
                                                        fighter2["sp"])["stats"]["spa"]
                                                    if fighter2["sp"] == "Bloodmage":
                                                        spa += int(0.5 * (hps[3] - hps[2]))
                                                    elif fighter2["sp"] == "Bloodmage+":
                                                        spa += int(0.6 * (hps[3] - hps[2]))
                                                    elif fighter2["sp"] == "Bloodmage++":
                                                        spa += int(0.7 * (hps[3] - hps[2]))

                                                    # si on peut se heal l'équivalent de 1,.. tours de dégâts quand on est midlife, c'est worth

                                                    if hps[2] * 2 < hps[3] and heal(hps[2], hps[3], spa) - hps[2] > dmg + psnDmg + 7:
                                                        hps[2] = heal(
                                                            hps[2], hps[3], spa)
                                                        manacost = 6
                                                        if fighter2["sp"] == "Sorcier":
                                                            manacost -= 1
                                                        elif fighter2["sp"] == "Sorcier+":
                                                            manacost -= 2
                                                        elif fighter2["sp"] == "Sorcier++":
                                                            manacost -= 3
                                                        manas[3] -= 1
                                                        healing = True

                                        manas[2] -= manacost

                                        if manas[2] < manas[3]:
                                            manas[2] += 1

                                        if not healing:
                                            if atktype == 1 and "Alchimiste" in fighter2["sp"]:
                                                p1Psn += 1
                                            dmg = damage.dmg
                                            battledesc = ""

                                            if damage.crit:
                                                battledesc += "Coup critique! "
                                                dmg = max(int(dmg * 0.7), 1)
                                            battledesc += fighter2["name"] + " inflige " + str(
                                                dmg) + " dégâts à l'aide d'" + atkdesc + "! "

                                            if p1Psn > 0:

                                                if fighter2["sp"] == "Alchimiste++":
                                                    psnDmg = int(
                                                        hps[1] * 8 * p1Psn / 100)
                                                elif fighter2["sp"] == "Alchimiste++":
                                                    psnDmg = int(
                                                        hps[1] * 6.5 * p1Psn / 100)
                                                else:
                                                    psnDmg = int(
                                                        hps[1] * 5 * p1Psn / 100)

                                                battledesc += user.name + " subit " + \
                                                    str(psnDmg) + \
                                                " dégâts de poison!"
                                                hps[0] -= psnDmg

                                            hps[0] -= dmg

                                            if vmpHeal:
                                                if fighter2["sp"] == "Vampire++":
                                                    hps[2] = min(hps[3], int(
                                                        hps[2] + 0.8 * dmg))
                                                elif fighter2["sp"] == "Vampire+":
                                                    hps[2] = min(hps[3], int(
                                                        hps[2] + 0.65 * dmg))
                                                else:
                                                    hps[2] = min(hps[3], int(
                                                        hps[2] + 0.5 * dmg))
                                        else:
                                            battledesc = fighter2["name"] + \
                                                " se soigne!"

                                        if hps[0] > 0:

                                            names = user.name + \
                                                " VS " + fighter2["name"]

                                            newembed = createEmbed(firstturn, secondturn, names, lvl1, lvl2, hps[0], hps[1], hps[2], hps[
                                                                   3], manas[0], manas[2], manas[1], manas[3], battledesc, footertxt, True, p1Psn, p2Psn)

                                            await reaction.message.edit(embed=newembed)

                                        else:
                                            d = ""
                                            if damage.crit:
                                                d += "Coup critique! "
                                            d += str(fighter2["name"] + " a vaincu le joueur " + user.name + " avec " + str(
                                                hps[2]) + " HPs restants!")
                                            newembed = discord.Embed(
                                                colour=discord.Colour.purple(),
                                                title='Duel',
                                                description=d
                                            )

                                            if str(fighter2["name"]) == "Thomas":
                                                await user.kick()

                                            await reaction.message.edit(embed=newembed)

                                            while reaction.message.reactions != []:
                                                for areaction in reaction.message.reactions:
                                                    async for user in areaction.users():
                                                        await areaction.remove(user)

                                else:

                                    if isPve:
                                        desc = str(
                                            "Le joueur " + user.name + " a vaincu le monstre " + fighter2["name"])
                                    else:
                                        desc = str("<@!" + firstturn + ">, a triomphé de <@!" + secondturn + "> avec " + str(
                                            hps[2 * (pnumber - 1)]) + " HPs restants!")

                                    newembed = discord.Embed(
                                        colour=discord.Colour.purple(),
                                        title='Duel',
                                        description=desc
                                    )

                                    level1 = int(fighter1["stats"]["level"])
                                    level2 = int(fighter2["stats"]["level"])
                                    
                                    maxexp1 = calcExp(level1, level2)
                                    maxexp2 = calcExp(level2, level1)

                                    if isPve:
                                        exptogain = fighter2["stats"]["exp"]
                                    else:
                                        exptogain = int(((level2 + 6)/(level1 + 1)) * .1 * maxexp2 + 20)

                                    #Boucle inutile, je laisse en commentaire comme relique
                                    #for r in user.roles:
                                    #    if r.id == TUFFIGANG_R_ID:
                                    #        # confused stonks
                                    #        exptogain = int(exptogain * 1)

                                    exptogain = int(exptogain * fighter1["pstats"]["exp"])

                                    giveExp(firstuser, exptogain)

                                    newembed.add_field(name="Il gagne " + str(exptogain) + " points d'experience.", value= "\u200b", inline = False)

                                    if not isPve:
                                        exptolose = int(
                                            fighter2["stats"]["exp"]/2)
                                        game.halfExp(seconduser)
                                        newembed.add_field(name="Son adversaire perd " + str(exptolose) + " points d'experience.", value= "\u200b", inline = False)

                                    await reaction.message.edit(embed=newembed)

                                    while reaction.message.reactions != []:
                                        for areaction in reaction.message.reactions:
                                            async for user in areaction.users():
                                                await areaction.remove(user)

                        elif emoji == "broc":
                            if (manas[2 * (pnumber - 1)] >= 5 or (manas[2 * (pnumber - 1)] >= 4 and "Sorcier" in fighter1["sp"])) and hps[2 * (pnumber - 1)] != hps[1 + 2 * (pnumber - 1)]:
                                manas[2 * (pnumber - 1)] -= 5
                                if fighter1["sp"] == "Sorcier":
                                    manas[2 * (pnumber - 1)] += 1
                                elif fighter1["sp"] == "Sorcier+":
                                    manas[2 * (pnumber - 1)] += 2
                                elif fighter1["sp"] == "Sorcier++":
                                    manas[2 * (pnumber - 1)] += 3
                                manas[1 + 2 * (pnumber - 1)] -= 1
                                spa = fighter1["stats"]["spa"] + fighter1["weapon"]["spa"] + \
                                    game.getSP(fighter1["sp"])["stats"]["spa"]

                                if fighter1["sp"] == "Bloodmage":
                                    spa += int(0.5 * (hps[1 + 2 * (pnumber - 1)] - hps[2 * (pnumber - 1)]))
                                elif fighter1["sp"] == "Bloodmage+":
                                    spa += int(0.6 * (hps[1 + 2 * (pnumber - 1)] - hps[2 * (pnumber - 1)]))
                                elif fighter1["sp"] == "Bloodmage++":
                                    spa += int(0.7 * (hps[1 + 2 * (pnumber - 1)] - hps[2 * (pnumber - 1)]))

                                hps[2 * (pnumber - 1)] = heal(hps[2 * (pnumber - 1)],
                                                              hps[2 * (pnumber - 1) + 1], spa)
                                battledesc = user.name + " se soigne!"

                                lvl1 = str(fighter1["stats"]["level"])
                                lvl2 = str(fighter2["stats"]["level"])

                                names = embed.fields[0].name
                                if not isPve:
                                    newembed = createEmbed(secondturn, firstturn, names, lvl1, lvl2, hps[0], hps[1], hps[2], hps[
                                                           3], manas[0], manas[2], manas[1], manas[3], battledesc, footertxt, False, p1Psn, p2Psn)
                                else:
                                    newembed = createEmbed(firstturn, secondturn, names, lvl1, lvl2, hps[0], hps[1], hps[2], hps[
                                                           3], manas[0], manas[2], manas[1], manas[3], battledesc, footertxt, True, p1Psn, p2Psn)
                                await reaction.message.edit(embed=newembed)
                    else:
                        await reaction.remove(user)

                else:
                    await reaction.remove(user)


def heal(hp, maxhp, spa):
    return min(maxhp, int(hp + 5 + 2/10 * maxhp + spa))

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

            elif (emoji == 'arrow-right' and page_number < HELP_PAGES):
                pages.generate_embed(page_number + 1, embed)
            await message.edit(embed=embed)


@bot.command(name='help')
async def help(ctx):

    embed = discord.Embed(
        colour=discord.Colour.purple(),
        title='Trivial Bot help',
        description='Voici la liste des commandes utilisables!'
    )

    embed.set_footer(text='Page 1')

    pages.generate_embed(1, embed)  # generate page 1

    msg = await ctx.send(embed=embed)

    reactions = ['\U00002b05', '\U000027a1']  # :arrow-left: , :arrow-right:
    for emoji in reactions:
        await msg.add_reaction(emoji)


@bot.command(name='info')
async def info(ctx):
    embed = discord.Embed(
        colour=discord.Colour.purple(),
        title='Bot Sebastien Lefevre',
        description="Bot créé le 20/05/2020 à l'aide de discord.py suite à un amphi mémorable de Sébastien Lefèvre."
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
    number += random.randint(69, 420)
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
    number = ((((user_id) % USER_RATE_CONST1) % 169)/32)
    number = (int(20 * (number + 4.75)))/10
    return number


def rate2(user_id: int):
    number = ((((user_id) % USER_RATE_CONST2) % 169)/32)
    number = (int(20 * (number + 4.75)))/10
    return number


def rate3(user_id: int):
    number = ((((user_id) % USER_RATE_CONST3) % 169)/32)
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

            avg = int(100 * (note1 + note2 + note3) / 3) / 100

            msg = str("J'octroie à <@!" + str(mentionned_user) + "> la note de " + str(avg) + "/20.0 pour le projet de programmation:"
                      + "\n\n - Le cahier des charges remis était " + commentaire1 + ", et faisait " +
                      str(nbpages1) + " pages, il mérite donc la note de " + str(note1)
                      + "\n\n - Le cahier d'analyse et de conception remis était " + commentaire2 +
                      ", et faisait " + str(nbpages2) + " pages, il mérite donc la note de " + str(note2)
                      + "\n\n - Le rendu final était " + commentaire3 + ", et faisait " +
                          str(nbpages3) + \
                              " pages, il mérite donc la note de " + str(note3)
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
              "J'ai déjà répondu " +
              str(random.randint(69, 420)) + " fois à cette question!",
              "ANT c'est un super outil open source de la fondation Apache, qui permet de faire plein de commandes utiles que vous êtes incapables de taper vous-mêmes! Suffit de faire un build.xml, ça prend quoi, 1h?"
              ]
    response = random.choice(quotes)
    await ctx.send(response)


@bot.command(name='serverinfo')
async def serverinfo(ctx):
    guild = ctx.guild
    if (guild != None):
        ts = guild.created_at
        ts = ts.strftime('%Y-%m-%d %H:%M:%S')
        embed = discord.Embed(
            colour=discord.Colour.purple(),
            title=('Server info'),
            description=guild.description
        )
        embed.set_author(name=guild.name, icon_url= str(guild.icon_url))
        embed.add_field(name='Creation date', 
                        value=str(ts), 
                        inline=False)
        embed.add_field(name='Member count', 
                        value=str(guild.member_count), 
                        inline=False)
        embed.add_field(name='Region', 
                        value=str(guild.region), 
                        inline=False)
        embed.add_field(name='Custom emoji count', 
                        value=str(len(guild.emojis)), 
                        inline=False)
        embed.add_field(name='Owner',
                        value=str(guild.owner), 
                        inline=False)

        await ctx.send(embed=embed)


@bot.command(name='ss')
async def showstats(ctx):
    useri = ctx.message.author.id
    user = game.getUserData(useri)
    stats = user["stats"]
    w = user["weapon"]
    embed = discord.Embed(
        colour=discord.Colour.purple(),
        title='Vos stats',
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

    embed.add_field(name=('Level ' + str(level)),
                    value=("HP " + str(hp)), 
                    inline=False)
    embed.add_field(name=('Attaque ' + str(atk) + "  [ +" + atkbonus + " ] (atk)"), 
                    value=("Defense " + str(de) + "  [ +" + defbonus + " ] (def)"), 
                    inline=False)
    embed.add_field(name=('Att. Spe ' + str(spa) + "  [ +" + spabonus + " ] (spa)"), 
                    value=("Def. Spe " + str(spd) + "  [ +" + spdbonus + " ] (spd)"),
                    inline=False)
    embed.add_field(name='Vitesse ' + str(spe) + "  [ +" + spebonus + " ] (spe)",
                    value=f"Points de stats restants f{str(statpoints)}",
                    inline=False)
    embed.add_field(name=('Exp : ' + str(exp) + " / " + str(maxexp)),
                    value=bar, 
                    inline=False)
    await ctx.send(embed=embed)


@bot.command(name='sw')
async def showweaponstats(ctx):
    useri = ctx.message.author.id
    user = game.getUserData(useri)
    weapon = user["weapon"]
    embed = discord.Embed(
        colour=discord.Colour.purple(),
        title='Votre arme',
    )
    nom = weapon["name"]
    atk = weapon["atk"]
    de = weapon["def"]
    spa = weapon["spa"]
    spd = weapon["spd"]
    spe = weapon["spe"]

    embed.add_field(name=('Nom : ' + nom), 
                    value="-----------", 
                    inline=False)
    embed.add_field(name=('Attaque ' + str(atk)),
                    value=("Defense " + str(de)), 
                    inline=False)
    embed.add_field(name=('Att. Spe ' + str(spa)),
                    value=("Def. Spe " + str(spd)), 
                    inline=False)
    embed.add_field(name=('Vitesse ' + str(spe)),
                    value="-----------", 
                    inline=False)

    await ctx.send(embed=embed)


@bot.command(name='up')
async def usepoint(ctx, *args):
    useri = ctx.message.author.id

    try:
        stat = args[0]
        amount = 1
        try:
            amount = int(args[1])
        except:
            pass
        if stat in ["hp", "atk", "def", "spa", "spd", "spe"]:
            if game.increaseStat(useri, stat, amount):
                if (stat == "hp"):
                    amount *= 2
                response = f"La stat de {stat} a ete augmentée de {str(amount)}"
            else:
                response = "Une erreur s'est produite en tentant d'augmenter votre stat"
        else:
            response = "Indiquez une stat valide (hp, atk, def, spa, spd, spe)"
    except Exception as e:
        response = 'lefevre up <stat> [amount]'
    finally:
        await ctx.send(response)


@bot.command(name='duel')
async def duel(ctx, *args):
    embed = None
    valid = False
    try:
        mentionned_user = ctx.message.mentions[0]
        useri1 = ctx.message.author.id
        useri2 = mentionned_user.id

        if useri1 != useri2:

            user1 = game.getUserData(useri1)
            user2 = game.getUserData(useri2)

            embed = discord.Embed(
                colour=discord.Colour.purple(),
                title='Duel',
                description="Loading"
            )
            response = ""

            valid = True

        else:
            response = "Vous ne pouvez pas vous battre en duel contre vous-même!"
    except:
        response = "lefevre duel @User"
    finally:
        msg = await ctx.send(response, embed=embed)
        if valid:
            newembed = discord.Embed(
                colour=discord.Colour.purple(),
                title='Duel',
                description=str("<@!" + str(useri1) + "> a provoque <@!" + str(useri2) + "> en duel!")
            )

            level1 = int(user1["stats"]["level"])
            level2 = int(user2["stats"]["level"])
            exptogain1 = calcExp(level1, level2)
            exptogain2 = calcExp(level2, level1)

            newembed.add_field(name=(ctx.message.author.name + " est niveau " + str(level1) + "."), value = "Il pourrait gagner " + str(exptogain1) + " exp!", inline = False)
            newembed.add_field(name=(mentionned_user.name + " est niveau " + str(level2) + "."), value =  "Il pourrait gagner " + str(exptogain2) + " exp!", inline = False)
            await msg.edit(embed=newembed)
            # :white_check_mark: , :x:
            reactions = ['\U00002705', '\U0000274C']
            for emoji in reactions:
                await msg.add_reaction(emoji)


def getHp(hpembed1, hpembed2):
    hpembed1 = " ".join(hpembed1.split())
    hpembed2 = " ".join(hpembed2.split())
    hp1 = int(hpembed1.split(' ')[1])
    maxhp1 = int(hpembed1.split(' ')[3])
    hp2 = int(hpembed2.split(' ')[1])
    maxhp2 = int(hpembed2.split(' ')[3])
    return [hp1, maxhp1, hp2, maxhp2]


def getMana(manaembed1, manaembed2):
    manaembed1 = " ".join(manaembed1.split())
    manaembed2 = " ".join(manaembed2.split())
    mana1 = int(manaembed1.split(' ')[1])
    maxmana1 = int(manaembed1.split(' ')[3])
    mana2 = int(manaembed2.split(' ')[1])
    maxmana2 = int(manaembed2.split(' ')[3])
    return [mana1, maxmana1, mana2, maxmana2]


def dmgCalc(attacker, defender, w, hpAtk):
    return Dmg(attacker, defender, w, hpAtk)


@bot.command(name='pve')
async def pve(ctx, *args):
    useri1 = ctx.message.author.id
    user1 = game.getUserData(useri1)
    if (game.canPve(useri1)):
        if user1["stats"]["statpoints"] <= 10:

            ennemy = game.randomEnnemy(user1)

            sp1 = game.getSP(user1["sp"])
            sp2 = game.getSP(ennemy["sp"])

            maxhp1 = user1["stats"]["hp"] + sp1["stats"]["hp"]

            hp1 = maxhp1
            hp2 = ennemy["stats"]["hp"] + sp2["stats"]["hp"]

            speed1 = user1["stats"]["spe"] + \
                user1["weapon"]["spe"] + sp1["stats"]["spe"]
            speed2 = ennemy["stats"]["spe"] + \
                ennemy["weapon"]["spe"] + sp2["stats"]["spe"]

            if speed1 < speed2:
                damage = dmgCalc(ennemy, user1, 2, hp2)
                dmg = max(1, int(0.5 * damage.dmg))
                battledesc = ""

                if damage.crit:
                    battledesc += "Coup critique! "
                battledesc += ennemy["name"] + " inflige " + \
                    str(dmg) + " dégâts à l'aide d'un coup sournois!"

                hp1 = max(1, hp1 - dmg)

            else:
                battledesc = "Le combat vient de commencer, on souhaite bonne chance au joueur humain " + \
                    ctx.message.author.name + "."

            firstturn = str(useri1)
            secondturn = ennemy["name"]

            lvl1 = str(user1["stats"]["level"])
            lvl2 = str(ennemy["stats"]["level"])

            footer = "PVE"

            names = ctx.message.author.name + " VS " + ennemy["name"]

            embed = createEmbed(firstturn, secondturn, names, lvl1, lvl2, hp1,
                                maxhp1, hp2, hp2, 10, 10, 10, 10, battledesc, footer, True, 0, 0)

            msg = await ctx.send(embed=embed)

            reacts = ["\U00002694", "\U0001FA84", "\U0001F5E1", "\U0001F966"]

            for r in reacts:
                await msg.add_reaction(r)
        else:
            msg = await ctx.send("Vous avez beaucoup de points de stats à dépenser. Faites `lefevre up <stat> <amount>` pour améliorer vos stats, visibles avec la commande `lefevre ss`.")
    else:
        embed = discord.Embed(
            colour=discord.Colour.purple(),
            title='PVE',
            description=str(
                "Vous n'avez pas d'ennemi à affronter, revenez plus tard!")
        )

        await ctx.send(embed=embed)


@bot.command(name='pveamount')
async def pveamount(ctx):
    msg = str("Vous avez " + str(game.amountOfPveBattles(ctx.message.author.id)) + " combats restants.")
    await ctx.send(msg)


@bot.command(name='cw')
async def changeweapon(ctx):
    embed = createWeaponEmbed(ctx.message.author.id, 1)

    msg = await ctx.send(embed=embed)

    reacts = ["\U000025C0", "\U000026A1",
              "\U0001F525", "\U0001F4A7", "\U000025B6"]

    for r in reacts:
        await msg.add_reaction(r)


@bot.command(name='leaderboard')
async def leaderboard(ctx):
    embed = discord.Embed(
        colour=discord.Colour.purple(),
        title='Leaderboard',
        description="Classement des joueurs les plus haut niveau"
    )

    lead = game.getBestPlayers()

    for idx, u in enumerate(lead):
        duser = await bot.fetch_user(u[0])
        embed.add_field(name=str(duser), value= str("#" + str(idx+1) + " Level " + str(u[1])), inline = False)

    await ctx.send(embed=embed)


@bot.command(name='resetstats')
async def resetstats(ctx):
    game.resetStats(ctx.author.id)
    msg = str("Vos stats ont été réinitialisées!")
    await ctx.send(msg)


@bot.command(name='secret')
async def secret(ctx):
    msg = str("Cette commande ne sera disponible qu'à partir du 29 Janvier.") # On est le 17 février là quand meme
    await ctx.send(msg)


@bot.command(name='sellcurrweapon')
async def sellCurrentWeapon(ctx):
    success, exp = game.sellWeapon(ctx.author.id)
    if success:
        msg = str("Votre arme a ete vendue pour " + str(exp) + "exp!")
    else:
        msg = str("Une erreur est survenue pendant la vente de votre arme.")
    await ctx.send(msg)


splist1 = ['Assassin', 'Alchimiste', 'Battlemage',
           'Berserker', 'Bloodmage', 'Sorcier', 'Vampire']
splist = ', '.join(splist1)


@bot.command(name='sp')
async def sp(ctx, *args):
    embed = discord.Embed(
        colour=discord.Colour.purple(),
        title='Spécialité'
    )
    try:
        spname = args[0].capitalize()
        if spname in splist1:
            sp = game.getSP(spname)
            embed = makeSPEmbed(sp, embed)
        else:
            embed.add_field(name="Cette spécialité n'existe pas!", value= "Liste des sps actuelles : " + splist, inline = False)
    except:
        useri1 = ctx.message.author.id
        user1 = game.getUserData(useri1)
        sp = user1["sp"]
        if user1["stats"]["level"] < 30:
            embed.add_field(name="Vous n'avez pas accès à cette fonctionnalité pour l'instant!", value= "Montez d'abord niveau 30.", inline = False)
        elif sp == "None":
            embed.add_field(name="Vous n'avez pas de spécialité! Tapez lefevre spec <nom de la specialité> pour vous spécialiser!", value= "Liste des sps actuelles : " + splist, inline = False)
        else:
            embed = makeSPEmbed(game.getSP(sp), embed)
    finally:
        await ctx.send(embed=embed)


@bot.command(name='spec')
async def spec(ctx, *args):
    try:
        spname = args[0].capitalize()
        if spname in splist1:
            if game.chgSpec(ctx.message.author.id, spname):
                msg = "Vous avez changé de specialité!"
            else:
                msg = "Vous ne pouvez pas changer de spécialité car vous n'êtes pas niveau 30!"
        else:
            msg = "Une erreur est survenue lors de la séléction de votre spécialité. Veuillez utiliser la commande `lefevre spec <specialite>` avec une des spécialités suivantes : " + splist
    except:
        msg = "Une erreur est survenue lors de la séléction de votre spécialité. Veuillez utiliser la commande `lefevre spec <specialite>` avec une des spécialités suivantes : " + splist
    finally:
        await ctx.send(msg)


@bot.command(name='ban')
async def ban(ctx, *args):
    try:
        mentionned_user = ctx.message.mentions[0]
        useri1 = ctx.message.author.id
        ids = [143350417093296128, 135321090699427840]
        if useri1 in ids and mentionned_user!=useri1:
            # C'EST UN KICK PAS UN BAN OK JE FAIS PAS DES PRANKS DE BATARD NON PLUS
            await mentionned_user.kick()
            response = "ok bro"
        else:
            response = "t'es qui en fait"
    except:
        response = "bah non du coup"
    finally:
        msg = await ctx.send(response)


@bot.command(name='prestige')
async def prestige(ctx):
    useri = ctx.message.author.id
    user = game.getUserData(useri)
    if user["stats"]["level"] < 50:
        await ctx.send("Vous ne pouvez pas prestige car vous n'avez pas encore atteint le niveau 50.")
    else:

        pgain = getPrestigeGain(user)

        embed = discord.Embed(
            colour=discord.Colour.purple(),
            title=('Prestige'),
        )
        embed.add_field(name='Voulez-vous vraiment prestige ?',
                        value="\u200b",
                        inline=False)
        embed.add_field(name='Vous recommencerez au niveau 0, en perdant votre équipement et votre spécialité.',
                        value="\u200b",
                        inline=False)
        embed.add_field(name='Vous obtiendrez ' + str(pgain) + ' points de prestige.',
                        value="Si vous êtes sûr de vouloir prestige, faites `lefevre prestigeconfirm`.",
                        inline=False)
        await ctx.send(embed=embed)


@bot.command(name='prestigeconfirm')
async def prestigeconfirm(ctx):
    useri = ctx.message.author.id
    user = game.getUserData(useri)
    if user["stats"]["level"] < 50:
        await ctx.send("Vous ne pouvez pas prestige car vous n'avez pas encore atteint le niveau 50.")
    else:

        pgain = getPrestigeGain(user)
        game.givePrestige(useri, pgain)
        await ctx.send("Vous êtes revenus au niveau 0, avec un gain de " + str(pgain) + " points de prestige!")


def costs(user):
    pperks = user["pperks"]

    expLvl = pperks["exp"]
    statLvl = pperks["stats"]
    spLvl = pperks["sp"]

    BASE_EXP_COST = 10
    BASE_STAT_COST = 2
    BASE_SP_COST = 35

    expCost = int(BASE_EXP_COST * (1.5 * (expLvl + 1)))

    statCost = int(BASE_STAT_COST * 1.5 * statLvl)

    spCost = int(BASE_SP_COST * ((spLvl + 1) ** 1.6))

    return expCost, statCost, spCost


@bot.command(name='pshop')
async def prestigeshop(ctx):
    useri = ctx.message.author.id
    user = game.getUserData(useri)

    eCost, stCost, spCost = costs(user)

    embed = discord.Embed(
        colour=discord.Colour.purple(),
        title=('Prestige Shop'),
        description='Vous avez ' + str(user["ppoints"]) + ' points de prestige à dépenser.'
    )

    pperks = user["pperks"]

    expLvl = pperks["exp"]
    statLvl = pperks["stats"]
    spLvl = pperks["sp"]

    exp_mul = 1 + 0.5 * expLvl
    nexp_mul = 1.5 + 0.5 * expLvl

    sBonus = statLvl * 5

    embed.add_field(name="Multiplicateur d'experience actuel : " + str(exp_mul),
                    value="Suivant : " + str(nexp_mul) + " Cout : " + str(eCost), 
                    inline=False)
    embed.add_field(name="Bonus de stats actuel (pour toutes les stats) : " + str(sBonus),
                    value="Suivant : " + str(sBonus + 5) + " Cout : " + str(stCost), 
                    inline=False)
    if spLvl < MAX_SP_TIER:
        embed.add_field(name="Tier des spécialités déverouillées : " + str(spLvl), 
                        value="Suivant : " + str(spLvl + 1) + " Cout : " + str(spCost) + " Max : " + str(MAX_SP_TIER),
                        inline=False)
    embed.add_field(name='Pour dépenser vos points de prestiges, utilisez la commande `lefevre pbuy <item>`',
                    value="<item> : (sp | exp | stats)",
                    inline=False)

    await ctx.send(embed=embed)


@bot.command(name='pbuy')
async def pbuy(ctx, *args):
    try:
        item = args[0]
        if item in ['sp', 'exp', 'stats']:
            if game.upPres(ctx.message.author.id, item, costs(game.getUserData(ctx.message.author.id))):
                msg = "Achat réussi."
            else:
                msg = "Vous n'avez pas assez de points pour cet item, ou vous êtes déjà au niveau de récompense maximum."
        else:
            msg = "`lefevre pbuy <item>` avec `<item> : (sp | exp | stats)`"
    except Exception as e:
        msg = "Une erreur est survenue lors de l'achat. Avez vous bien fait `lefevre pbuy <item>` avec `<item> : (sp | exp | stats)` ?"
    finally:
        await ctx.send(msg)


@bot.command(name='abusereset')
async def abusereset(ctx, *args):
    response = ""
    try:
        userid = ctx.message.author.id
        if userid == 143350417093296128 or userid == GABRIEL_ID:
            try:
                abuser = ctx.message.mentions[0]
                abuserid = abuser.id
                #On reset les stats
                game.resetStats(abuserid)
                game.resetUser(abuserid)
                game.setPrestige(abuserid, 200)
                await ctx.send("Vous etes revenus a 0 !\nIl vous reste 200 points de prestige")
            except:
                await ctx.send("Syntaxe: lefevre abusereset @User")
        else:
            await ctx.send("Bonsoir non")
    except:
        await ctx.send("W00dy sait pas coder :(")


@bot.command('bde')
async def bde(ctx):
    list = ['BrHackage', 'Je s\'appelle Root', 'DrHackon']
    await ctx.send('Votez ' + random.choice(list) + ' !')

@bot.command('toggleinsults')
async def toggleinsults(ctx):
    response = "C'est pas toi qui decide !"
    if ctx.message.author.id == GABRIEL_ID:
        INSULTES_ACTIVATED = not INSULTES_ACTIVATED
        response = "Pas de probleme khet"
    await ctx.send(response)


@tasks.loop(seconds=3600)
async def insulte_tuffigang():
    channel = bot.get_channel(TUFFIGANG_C_ID)
    tuffig = channel.guild.get_role(TUFFIGANG_R_ID)
    if tuffig != None and INSULTES_ACTIVATED:
        members = channel.members
        tuffimembers = []
        for member in members :
            if tuffig in member.roles and member.status!=discord.Status.offline and not member.bot and member.id != 315199843238805504:
                tuffimembers.append(member)
        if tuffimembers != []:
            chosen_user = random.choice(tuffimembers)

            insultes = ["Va te faire cuire un oeuf", "Espèce de fan d'Ecobosto",
                        "On est obligés de compter en base 3 pour que tu aies un QI à 3 chiffres",
                        "T'es un peu cringe", "Bannez moi ça les admins :",
                        "Get gulaged", "je te ban en fait", "rôle pedance direct",
                        "Marin d'eau douce", "Petit gougnafier", "Sale goujat",
                        "Pauvre Bélître", "Tu n'est qu'un Butor", "Vote Brhackage", "Fieffé Faquin",
                        "Orchidoclaste", "Méchant Fripon", "je vais vous ban, toi et ta bande de malapris,",
                        "Tu n'est qu'un simple Olibrius", "Visiblement, depuis le début du confinement tu vois plus souvent ta mère sur PHub qu'en vrai",
                        "Petit con", "Je te signale au secrétariat"]

            msg = random.choice(insultes) + ' <@!' + str(chosen_user.id) + '>'
            await channel.send(msg)

@tasks.loop(seconds=3600)
async def image_tuffigang():
    channel = bot.get_channel(TUFFIGANG_C_ID)
    if not INSULTES_ACTIVATED:
        photo = get_random_photo()
        await channel.send(photo)



bot.run(TOKEN)
