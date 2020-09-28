# bot.py
import os
import random
import pages
import discord
from discord.ext import commands
from dotenv import load_dotenv

HELP_PAGES = 2

USER_RATE_CONST = 417948452

SHIP_RATE_CONST = 9090338

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

BOT_ID = int(os.getenv('BOT_ID'))


bot = commands.Bot(command_prefix='lefevre ')
bot.remove_command('help')




@bot.event
async def on_ready():
    myActivity = discord.Game("'lefevre help' pour la liste de commandes!")
    await bot.change_presence(status=discord.Status.dnd, activity=myActivity)
    print("C'est trivial")


@bot.event
async def on_message(message: discord.Message):
    process = True
    if message.guild is None and not message.author.bot:
        response = "Hop hop hop, on n'envoie pas de messages privés. Si tu as une question, il faut la poser sur le forum!"
        chan = message.channel
        await chan.send(response)
        process = False

    if not message.author.bot and len(message.mentions) > 0 :
        if str(message.mentions[0].id) == str(BOT_ID) :
            response = "Debrouille-toi."
            chan = message.channel
            await chan.send(response)

    if (process) :
        await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    emoji = ''
    if(reaction.emoji == '⬅'):
        emoji = 'arrow-left'
    if(reaction.emoji == '➡'):
        emoji = 'arrow-right'
    if (reaction.count != 1 and emoji != ''):
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
async def forum(ctx):
    response = "ANT c'est un super outil open source de la fondation Apache, qui permet de faire plein de commandes utiles que vous êtes incapables de taper vous-mêmes! Suffit de faire un build.xml, ça prend quoi, 1h?"
    await ctx.send(response)


@bot.command(name='travail')
async def travail(ctx):
    response = "Vous avez autant de travail qu'en temps normal. N'oubliez pas de passer votre week-end sur le TP!"
    await ctx.send(response)


@bot.command(name='random')
async def randomQuote(ctx):
    quotes = ["Swing est la meilleure librairie graphique de tous les langages de programmation possibles et imaginables. Il s'agit d'une technlogie jeune et souple utilisée partout dans le monde!",
              "Si vous avez une question, utilisez les forums moodle! Après tout vous n'êtes jamais là sur le chat sur les créneaux prévus ...",
              "Vous avez autant de travail qu'en temps normal. N'oubliez pas de passer votre week-end sur le TP!",
              "Va voir la javadoc",
              "J'ai déjà répondu " + str(random.randint(69,420)) + " fois à cette question!"
    ]
    response = random.choice(quotes)
    await ctx.send(response)



bot.run(TOKEN)
