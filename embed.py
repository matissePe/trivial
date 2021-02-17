import discord
import game


def createWeaponEmbed(userID, pageNumber):
    embed = discord.Embed(
        colour=discord.Colour.purple(),
        title='Inventaire',
        description=str("Voici l'inventaire de <@!" + str(userID) + ">")
    )

    fields = game.retInventory(userID, pageNumber - 1)

    emojis = [":zap:", ":fire:", ":droplet:"]

    if fields != None:
        for idx, f in enumerate(fields):
            embed.add_field(name=f, value= "Equippez l'arme en reagissant avec " + emojis[idx+1], inline = False)

    fi = game.fullInventory(userID)
    nbPages = int(1 + (len(fi) - 1) / 3)

    ft = str("Page " + str(pageNumber) + " / " + str(nbPages))

    embed.set_footer(text=ft)

    return embed


def createEmbed(firstturn, secondturn, names, lvl1, lvl2, hp1, maxhp1, hp2, maxhp2, mana1, mana2, maxmana1, maxmana2, battledesc, footer, isPve, p1Psn, p2Psn):
    if isPve:
        mydesc = str("<@!" + firstturn + ">, choisis une attaque! " + secondturn + " se défend.")
    else:
        mydesc = str("<@!" + firstturn + ">, choisis une attaque! <@!" + secondturn + "> se défend.")

    newembed = discord.Embed(
        colour=discord.Colour.purple(),
        title='Duel',
        description=mydesc
    )

    hpbar1 = "█" * int(10 * hp1/maxhp1) + "░" * (10 - int(10 * hp1/maxhp1))
    hpbar2 = "█" * int(10 * hp2/maxhp2) + "░" * (10 - int(10 * hp2/maxhp2))

    manabar1 = "█" * int(10 * mana1/10) + "░" * (10 - int(10 * mana1/maxmana1))
    manabar2 = "█" * int(10 * mana2/10) + "░" * (10 - int(10 * mana2/maxmana2))

    newembed.add_field(name=names, value= "Lvl " + lvl1 + " VS Lvl " + lvl2, inline = False)
    newembed.add_field(name="HP[" + str(p1Psn) + "] " + str(hp1) + " / " + str(maxhp1), value= hpbar1, inline = True)
    newembed.add_field(name="HP[" + str(p2Psn) + "] " + str(hp2) + " / " + str(maxhp2), value= hpbar2, inline = True)
    newembed.add_field(name='\u200b', value = '\u200b', inline = True)
    newembed.add_field(name="Mana " + str(mana1) + " / " + str(maxmana1), value= manabar1, inline = True)
    newembed.add_field(name="Mana " + str(mana2) + " / " + str(maxmana2), value= manabar2, inline = True)
    newembed.add_field(name='\u200b', value= '\u200b', inline = True)
    newembed.add_field(name="- - - - - - - - - - - - - - - - - - - - - - - - - - - - -", value= "\u200b", inline = False)
    newembed.add_field(name=":crossed_swords: Attaque physique        :magic_wand: Attaque magique", value= "\u200b", inline = False)
    newembed.add_field(name=":dagger: Coup sournois             :broccoli: Sort de soin", value= "\u200b", inline = False)
    newembed.add_field(name="- - - - - - - - - - - - - - - - - - - - - - - - - - - - -", value= "\u200b", inline = False)
    newembed.add_field(name=battledesc, value= "\u200b", inline = False)
    newembed.set_footer(text=footer)

    return newembed