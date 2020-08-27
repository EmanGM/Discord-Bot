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


@bot.command(name = 'identifica-te')
async def mensagem_resposta(ctx):

    await ctx.send("Eu sou um bot criado pelo Deus Eman!")


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
