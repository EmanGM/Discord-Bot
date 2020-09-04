import os

import random

import discord
from discord.ext import commands

#from dotenv import load_dotenv, find_dotenv

#variáveis deveriam ser descarregadas a partir do ficheiro .env
#mas não condigo pôr isso a funcionar
#load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

TOKEN = 'NzM0NDkzNjEwMDc4MTA5NzI3.XxSgeg.FShbtoPETMDrplvWN0TQmxRsCeg'
#GUILD = 'RealPythonTutorialBotServer'
GUILD = "☭ USSR ☭"

bot = commands.Bot(command_prefix = '!')

"""
@bot.event
async def on_ready():

    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{bot.user.name} has connected to Discord!\n'
          f'{guild.name}(id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Pessoal deste servidor:\n - {members}')

"""
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Boooooas {member.name}, welcome to Russia Discord server!')


@bot.command(name = 'puta')
async def mensagem_resposta(ctx):

    brooklyn_99_quotes = ['Prazer em conhecer-te, posso-te ir ao cúe?']

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
   # elif message.content == "levantar erro!":
    #    raise discord.DiscordException

@bot.command(name = 'hello')
async def mensagem_resposta(ctx):

    await ctx.send("Ora boas!")

@bot.command(name = 'micas')
async def mensagem_resposta(ctx):

    await ctx.send("Miau!")

@bot.command(name = 'imagem')
async def mensagem(ctx):

    await ctx.send(file=discord.File('gorila.jpg'))


@bot.command(name = 'identifica-te')
async def mensagem_resposta(ctx):

    await ctx.send("Eu sou um bot criado pelo Deus Eman!")

def is_me(m):
    return m.author == bot.user

@bot.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount, check = is_me)
    await ctx.send("Fiz-te o favor e apagei {} mensagens.".format(amount))


@bot.command()
async def embed(ctx):
    embed = discord.Embed(title = ">Caixa", description = "teste", colour = discord.Colour.orange())
    embed.set_footer(text = "rodapé")
    embed.set_image(url = "https://static.dicionariodesimbolos.com.br/upload/8e/29/laranja-1_xl.png")
    embed.set_author(name = "O próprio! ")
    embed.set_thumbnail(url = 'https://static.dicionariodesimbolos.com.br/upload/8e/29/laranja-1_xl.png')
    embed.add_field(name = "comandos", value = "todos os possíveis")
    embed.add_field(name = "copos", value = "qualquer um", inline = True)

    await ctx.send(embed = embed)


@bot.event
async def on_error(evento, *args, **kargs):
    with open("err.log", 'a') as f:
        if evento == 'on_message':
            f.write(f'Mensagem desconhecida: {args[0]}\n')
        else: 
            raise

@bot.command(name = "dados")
async def roll(ctx, n_dados: int, n_faces: int):
    dado = [str(random.choice(range(1, n_faces + 1))) for _ in range(n_dados)]
    await ctx.send(", ".join(dado))




bot.run(TOKEN)
