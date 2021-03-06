import discord
from discord.voice_client import VoiceClient
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import ffmpeg
import youtube_dl
from random import choice
import asyncio
from discord.utils import get
import requests
from bs4 import BeautifulSoup
import aternosapi 

client = commands.Bot(command_prefix='Brek ', case_insensitive=False )

@client.command(help="ip servera", aliases= ["mc", "minecraft",],)
async def ip(ctx):
	await ctx.send("pajace_na.aternos.me")

@client.command(help='ping - pong')
async def ping(ctx):
    await ctx.send(f'PONG! {round(client.latency * 1000)}ms')

@client.event
async def on_command_error(ctx, error,):
	if isinstance(error, commands.errors.CommandNotFound):
			await ctx.send("Rub mie louda")

@client.command(help='kabulon',)
async def kabulon(ctx):
	await ctx.send("gówno z cebulom")

@client.command(help='pull-up', aliases= ["pulla", "pull-up", "pul-up",],)
async def pula(ctx):
	await ctx.send("pula, pula obciągasz mi siura")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Minecraft'))
    print('Bot aktywowany')

@client.event
async def on_member_join(member):
    print(f'{member} dołączył do serwera')

@client.command(aliases= ['purge','delete'], help='clearuje 11 wiadomości, chyba że wpiszesz po clear liczbę (nie działa po clear liczb)')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=11): # Set default value as None
    if amount == None:
        await ctx.channel.purge(limit=1000000)
    else:
        try:
            int(amount)
        except: # Error handler
            await ctx.send('aha')
        else:
            await ctx.channel.purge(limit=amount)

#MUZYKA
#       MUZYKA
#              MUZYKA
#                     MUZYKA
#                            MUZYKA

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


@client.command(aliases = ["wejdź", "dołącz"], help='dodaje bota do kanału')
async def dolacz(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@client.command(name='zagraj', help='bot gra muzyke ')
async def zagraj(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send("No chyba nie, nie jesteś połączony do kanału")
        return

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('error plejera: %s' % e) if e else None)

    await ctx.send('**Widzisz mnie?** *teraz gram: * {}'.format(player.title))

@client.command(name='stop', help='ta komenda zatrzymuje muzyke')
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('stopowanie...')

@client.command(pass_context=True, aliases = ["wejdż", "wypierdalaj"])
async def wyjdz(ctx):
	server = ctx.message.guild.voice_client
	await server.disconnect()
	await ctx.send("no ok ):")

token = os.environ.get("TOKEN")
client.run(token)