import nextcord
from nextcord.ext import commands
import os 
import asyncio
import youtube_dl as ytdl

class Music(nextcord.Cog):
  def __init__(self, client):
    self.client = client
    self.voice_clients = {}
    self.yt_dl_opts = {
        'format': 'bestaudio/best'
    }
    self.ytdl = ytdl.YoutubeDL(yt_dl_opts)
    self.ffmpeg_options = {
        'options': '-vn'
    }
    
    @commands.Cog.listener()
    async def on_message(msg):
      if msg.content.startswith("play"):
        try:
          url = msg.content.split()[1]
          voice_client = await msg.author.voice.channel.connect()
          voice_clients[voice_client.guild.id] = voice_client
          
          loop = asyncio.get_event_loop()
          data = loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
          
          song = data['url']
          player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

          voice_clients[msg.guild.id].play(player)
            
          
        except Exception as err:
            print(err)
      
      if msg.content.startswith("?pause"):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)
       
       
      if msg.content.startswith("?stop"):
        try:
            voice_clients[msg.guild.id].stop()
            await voice_clients[msg.guild.id].disconnect()
        except Exception as err:
            print(err)
    
    
def setup(client):
  client.add_cog(Music(client))