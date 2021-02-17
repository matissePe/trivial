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