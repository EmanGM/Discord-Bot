import os

import random

import discord
from discord.ext import commands

import youtube_dl
import ffmpeg

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

@bot.command()
async def hello(ctx):

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


@bot.command()
async def func(ctx):
    if name == "3":
        await ctx.send("numero 3")


@bot.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)
    await ctx.send("Utilizaste o comando \"clear\" portanto fiz-te o favor e apagei {} mensagens.".format(amount))


@bot.command()
async def embed(ctx):
    embed = discord.Embed(title = ">Caixa", description = "teste", colour = discord.Colour.orange())
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


#music
@bot.command()
async def play(ctx, url : str):

    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
    YDL_OPTIONS = {'format':'bestaudio', 'default_search': 'auto'}

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, id = ctx.author.voice.channel.id)
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    #if not voice.is_connected():
        #await voiceChannel.connect()

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download = False)

        if 'formats' in info: #caso de pesquisa por url
            url2 = info['formats'][0]['url']
        elif 'entries' in info: #caso de pesquisa por palavras
            url2 = info['entries'][0]['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        voice.play(source)


@bot.command()
async def leave(ctx):

    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Não estou conectado a um canal!")

@bot.command()
async def pause(ctx):

    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        await voice.pause()
    else:
        await ctx.send("Não estou a exibir música")

@bot.command()
async def resume(ctx):
    
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        await voice.resume()
    else:
        await ctx.send("Não está nenhuma música em pausa")



@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    voice.stop()








bot.run(TOKEN)
