import os

import random
import asyncio

import discord
from discord.ext import commands

import youtube_dl
import ffmpeg

#from dotenv import load_dotenv, find_dotenv

#variáveis deveriam ser descarregadas a partir do ficheiro .env
#mas não consigo pôr isso a funcionar
#load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

TOKEN = 'NzM0NDkzNjEwMDc4MTA5NzI3.XxSgeg.kUEz2NJOuiKCSakFGNp8od5rxpE'


bot = commands.Bot(command_prefix = '.')

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
    #embed.set_image(url = "https://static.dicionariodesimbolos.com.br/upload/8e/29/laranja-1_xl.png")
    helpUI.set_image(url = 'https://drive.google.com/file/d/1-6g7UcvAHSsCX2nWFnodpaFQZ4unOyTO/view')
    #embed.set_author(name = "O próprio! ")
    #embed.set_thumbnail(url = 'https://static.dicionariodesimbolos.com.br/upload/8e/29/laranja-1_xl.png')
    helpUI.add_field(name = "clear [x]", value = "apaga x mensagens do chat (se x não for especificado elimina 5)", inline = False)
    helpUI.add_field(name = "play [url ou pesquisa]", value = "mete a música pretendida a tocar", inline = False) # inline = True
    helpUI.add_field(name = "pause", value = "mete a música em pausa", inline = False)
    helpUI.add_field(name = "resume", value = "tira a música da pausa", inline = False)
    helpUI.add_field(name = "leave", value = "desconectar-me de uma sala de voz", inline = False)
    helpUI.add_field(name = "skip", value = "elimina a música que está a tocar e apaga-a", inline = False)
    helpUI.add_field(name = "comandos", value = "mostra esta mensagem", inline = False)
    helpUI.set_footer(text = "qualquer outra coisa que peçam para eu fazer poderá não ter qualquer efeito")
    await ctx.send(embed = helpUI)


#music
@bot.command()
async def play(ctx, *url):

    if ctx.author.voice == None:
        await ctx.send("Não estás conectado a nenhuma sala de voz!")
        return

    if url == ():
        await ctx.send("Não especificaste a música que queres ouvir \uFE0F!")
        return
    str2search = ' '.join(url)

    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
    YDL_OPTIONS = {'format':'bestaudio', 'default_search': 'auto'}

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, id = ctx.author.voice.channel.id)
    try:
        await voiceChannel.connect()
    except:
        print("Error")
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)


    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(str2search, download = False)

        if 'formats' in info: #caso de pesquisa por url
            url2 = info['formats'][0]['url']
        elif 'entries' in info: #caso de pesquisa por palavras
            url2 = info['entries'][0]['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        voice.play(source)

    while True:
        await asyncio.sleep(20)

        if not voice.is_playing():
            await voice.disconnect()
            print("bot exit voice channel")
            break

@bot.event
async def on_voice_state_update(member, before, after):
    
    if member.id == bot.user.id:
        print("Bot triggered voice_changed event")
        #if before.voice.channel != None and after.voice.channel:
            #return
    else:
        print("Member {} in guild {} triggered voice_changed event".format(member, member.guild))
        if before.channel and after.channel == None:
            if len(before.channel.members) == 1:
                print("chat vazio")
                voice = discord.utils.get(bot.voice_clients, guild = member.guild)
                await voice.disconnect()

@bot.command()
async def leave(ctx):

    voice = ctx.voice_client
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Não estou conectado a um canal!")

@bot.command()
async def pause(ctx):

    voice = ctx.voice_client
    if voice == None or not voice.is_playing():
        await ctx.send("Não estou a exibir música")
    else: 
        voice.pause()
        await ctx.send("Música em Pausa \u23F8")


@bot.command()
async def resume(ctx):
    
    voice = ctx.voice_client
    if voice == None or not voice.is_paused():
        await ctx.send("Não está nenhuma música em pausa")
    else:
        voice.resume()
        await ctx.send("Música em play \u25B6")


@bot.command()
async def stop(ctx):
    voice = ctx.voice_client
    voice.stop()

@bot.command()
async def skip(ctx): #O objetivo é invokar a função stop
    voice = ctx.voice_client
    voice.stop()


bot.run(TOKEN)
