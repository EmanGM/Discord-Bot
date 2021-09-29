import discord
from discord.ext import commands

import asyncio
import youtube_dl
import ffmpeg


class Music(commands.Cog):

    def __init__(self, client):
        self.bot = client
        self.voice = None
        self.playList = []
        self.isPaused = False

    #Comandos
    @commands.command()
    async def add(self, ctx):
        await ctx.send("Comando inválido, utiliza antes '.play'")

    async def play_music(self, ctx):
        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
        self.playList[0]['message_id'] = await ctx.send("Agora a tocar {}: {}".format(self.playList[0]['title'], self.playList[0]['video_url']))
        source = await discord.FFmpegOpusAudio.from_probe(self.playList[0]['audio_url'], **FFMPEG_OPTIONS)
        self.voice.play(source)

    @commands.command()
    async def play(self, ctx, *url):

        if ctx.author.voice == None:
            await ctx.send("Não estás conectado a nenhuma sala de voz!")
            return

        if url == ():
            await ctx.send("Não especificaste a música que queres ouvir \uFE0F!")
            return
        str2search = ' '.join(url)

        YDL_OPTIONS = {'format':'bestaudio', 'default_search': 'auto'}

        voiceChannel = discord.utils.get(ctx.guild.voice_channels, id = ctx.author.voice.channel.id)
        try:
            await voiceChannel.connect()
        except:
            print("Já connectado a uma sala de voz")

         
        if self.voice != None:
            await ctx.send("Uma música já está a ser tocada. Música requisitada foi adicionada à fila. '.fila' para ver a lista de reprodução")
        self.voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)

        data2keep = dict()
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info("ytsearch:{}".format(str2search), download = False)

            if 'formats' in info: #caso de pesquisa por url
                data2keep['audio_url'] = info['formats'][0]['url']
                data2keep['title'] = info['formats'][0]['title']
                data2keep['video_url'] = info['formats'][0]['webpage_url']
            elif 'entries' in info: #caso de pesquisa por palavras
                data2keep['audio_url'] = info['entries'][0]['url']
                data2keep['title'] = info['entries'][0]['title']
                data2keep['video_url'] = info['entries'][0]['webpage_url']

        self.playList.append(data2keep)

        if not self.voice.is_playing(): 
            await self.play_music(ctx)

            while True:
                await asyncio.sleep(10)

                if not self.isPaused and not self.voice.is_playing():
                    #TODO: apagar mensagem
                    #message2delete = await discord.abc.Messageable.fetch_message(self, id = self.playList[0]['message_id'])
                    #await self.bot.delete_message(message2delete)
                    self.playList = [self.playList.pop()] if len(self.playList) > 1 else []
                    if not self.playList:
                        await self.voice.disconnect()
                        print("bot exit voice channel")
                        break
                    else:
                        await self.play_music(ctx)
    
   
    @commands.command()
    async def leave(self, ctx):

        if self.voice and self.voice.is_connected():
            await self.voice.disconnect()
        else:
            await ctx.send("Não estou conectado a um canal!")

    @commands.command()
    async def pause(self, ctx):

        if self.voice == None or not self.voice.is_playing():
            await ctx.send("Não estou a exibir música")
        else: 
            self.voice.pause()
            await ctx.send("Música em Pausa \u23F8")
            self.isPaused = True


    @commands.command()
    async def resume(self, ctx):
    
        if self.voice == None or not self.voice.is_paused():
            await ctx.send("Não está nenhuma música em pausa")
        else:
            self.voice.resume()
            await ctx.send("Música em play \u25B6")
            self.isPaused = False


    @commands.command()
    async def stop(self, ctx):
        
        if self.voice:
            self.voice.stop()
            self.playList = []

    @commands.command()
    async def skip(self, ctx):
        
        if self.voice:
            self.voice.stop()
            await ctx.send("Musica saltada \u23ED")

    @commands.command(name = "fila", aliases=["queue", "q", "lista"])
    async def fila(self, ctx):

        if self.playList:
            queue = discord.Embed(title = "Fila de reprodução", colour = discord.Colour.dark_orange())
            for i, music in enumerate(self.playList):
                queue.add_field(name = "{}) {}".format(i + 1, music['title']), value = music['video_url'], inline = False)

            await ctx.send(embed = queue)
        else:
            await ctx.send("Não existe nenhuma lista de reprodução")
    
    @commands.command(name = "DIGA")
    async def diga_um(self, ctx, um):
        if um == "UM":
            await ctx.invoke(self.bot.get_command('play'), "https://www.youtube.com/watch?v=HUtMwiCnVCE")


    #Eventos
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
    
        if member.id == self.bot.user.id:
            print("Bot triggered voice_changed event")
            #if before.voice.channel != None and after.voice.channel:
                #returnhe
        else:
            print("Member id {} in guild {} triggered voice_changed event".format(member.discriminator, member.guild))
            #Se for o Subtil ou o Ric, mandar mensagem
            if member.discriminator == '0017' or member.discriminator == '6077': 
                await member.create_dm()
                if before.channel == None:
                    emoji = discord.utils.get(self.bot.emojis, name=':money_mouth')
                    await member.dm_channel.send("Boas patinho:duck:  obelinha:sheep:!  :money_mouth:")
                elif after.channel == None:
                    emoji = discord.utils.get(self.bot.emojis, name=':pleading_face')
                    await member.dm_channel.send("Já bais, patinho:duck:  obelinha:sheep:?  :pleading_face:")
            if before.channel and after.channel == None:
                if len(before.channel.members) == 1 and self.voice != None:
                    print("chat vazio")
                    #voice = discord.utils.get(bot.voice_clients, guild = member.guild)
                    await self.voice.disconnect()



def setup(client):
    client.add_cog(Music(client))
