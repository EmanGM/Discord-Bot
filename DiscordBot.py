import os

import random
import asyncio

import discord
from discord.ext import commands


#from dotenv import load_dotenv, find_dotenv

#variáveis deveriam ser descarregadas a partir do ficheiro .env
#mas não consigo pôr isso a funcionar
#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix = '.')

def main():

    file = open("Variables.txt", "r")
    TOKEN = file.readline().strip()
    file.close()

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension("cogs.{}".format(filename[:-3]))

    bot.run(TOKEN)



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
    await member.dm_channel.send(f'Boooooas {member.name}, bem-vindo ao servidor {member.guild}!')


@bot.command(name = 'puta')
async def mensagem_resposta(ctx):

    quotes = ['Prazer em conhecer-te, posso-te ir ao cúe?']
    #ir buscar ideias a 'https://gist.github.com/inescoelho/4a2e848480d2026121f8d5c600ee3c66'

    response = random.choice(quotes)
    await ctx.send(response)
   # elif message.content == "levantar erro!":
    #    raise discord.DiscordException

@bot.command()
async def hello(ctx):

    await ctx.send("Ora boas!")


@bot.command(name = 'imagem')
async def mensagem(ctx):

    await ctx.send(file=discord.File('gorila.jpg'))


@bot.command(name = 'identifica-te')
async def mensagem_resposta(ctx):
    await ctx.send("Eu sou um bot criado pelo Deus Eman!")


@bot.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)
    await ctx.send("Utilizaste o comando \"clear\" portanto fiz-te o favor e apagei {} mensagens.".format(amount))

#Esta função é apenas um teste
@bot.command()
async def embed(ctx):
    embed = discord.Embed(title = "Caixa", description = "teste", colour = discord.Colour.orange())
    embed.set_footer(text = "rodapé")
    #embed.set_image(url = "https://static.dicionariodesimbolos.com.br/upload/8e/29/laranja-1_xl.png")
    embed.set_image(url = 'https://drive.google.com/file/d/1-6g7UcvAHSsCX2nWFnodpaFQZ4unOyTO/view')
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


@bot.command()
async def comandos(ctx):

    helpUI = discord.Embed(title = "Comandos disponíveis:", description = "", colour = discord.Colour.blurple())

    helpUI.add_field(name = "clear [x]", value = "apaga x mensagens do chat (se x não for especificado elimina 5)", inline = False)
    helpUI.add_field(name = "play [url ou pesquisa]", value = "mete a música pretendida a tocar", inline = False) # inline = True
    helpUI.add_field(name = "pause", value = "mete a música em pausa", inline = False)
    helpUI.add_field(name = "resume", value = "tira a música da pausa", inline = False)
    #helpUI.add_field(name = "leave", value = "desconectar-me de uma sala de voz", inline = False)
    helpUI.add_field(name = "skip", value = "salta para a música seguinte", inline = False)
    helpUI.add_field(name = "stop", value = "elimina todas as músicas da lista de reprodução", inline = False)
    helpUI.add_field(name = "fila", value = "visualizar a lista de reprodução", inline = False)
    helpUI.add_field(name = "DIGA UM", value = "comando auto explicativo", inline = False)
    helpUI.add_field(name = "comandos", value = "mostra esta mensagem", inline = False)
    helpUI.add_field(name = "\u200B", value = "Para fazer melhorias ou acrescentar funcionalidades, falar com o Eman ou então modifica-me em https://github.com/Eragon30/Discord-Bot")
    await ctx.send(embed = helpUI)



if __name__ == "__main__":
    main()
