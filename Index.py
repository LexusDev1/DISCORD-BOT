import nextcord
import databases
import dislevel
import os
import yaml
import asyncio
from colorama import Fore
from nextcord.ext import commands

with open("storage/configs/yaml/configs.yml", "r") as Discord:
    Configuration = yaml.safe_load(Discord)

TOKEN = Configuration['Discord']['TOKEN']
PREFIX = Configuration['Discord']['PREFIX']
CLIENT_ID = Configuration['SPOTIFY']['CLIENT_ID']
CLIENT_SECRET = Configuration['SPOTIFY']['CLIENT_SECRET']
HOST = Configuration['LAVALINK']['HOST']
PASSWORD = Configuration['LAVALINK']['PASSWORD']
PORT = Configuration['LAVALINK']['PORT']

intents = nextcord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)

async def load_cogs():
    for folder_name in os.listdir("./cogs"):
        folder_path = os.path.join("./cogs", folder_name)
        if os.path.isdir(folder_path):
            for subfolder_name in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder_name)
                if os.path.isdir(subfolder_path):
                    cog_files = [filename for filename in os.listdir(subfolder_path) if filename.endswith(".py")]
                    for filename in cog_files:
                        if filename == "__init__.py" or subfolder_name == "ffmpeg":
                            continue
                        try:
                            cog_path = f"cogs.{folder_name}.{subfolder_name}.{filename[:-3]}"
                            client.load_extension(cog_path)
                        except Exception as e:
                            print(f"Failed to load cog {cog_path}: {e}")

async def main():
    await load_cogs()
    await client.start(TOKEN)

asyncio.run(main())
