# bot.py
import os
import random
import pages
import discord
from discord.ext import commands
from dotenv import load_dotenv

HELP_PAGES = 2

USER_RATE_CONST1 = 267234

USER_RATE_CONST2 = 112680

USER_RATE_CONST3 = 130984

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



bot.run(TOKEN)
