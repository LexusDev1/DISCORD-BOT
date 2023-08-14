import os
import platform
import sys
import nextcord
from nextcord.ext import commands

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="info")
    async def info(self, interaction: nextcord.Interaction):
        guild = interaction.guild
        owner = guild.owner
        member_count = guild.member_count
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        roles_count = len(guild.roles) - 1  # Excluding @everyone role

        nextcord_version = nextcord.__version__
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        bot_version = "1.0"  # Replace with your bot's version
        bot_cwd = sys.path[0]  # Get the bot's current working directory

        # Get the list of files and folders in the bot's working directory
        bot_files = os.listdir(bot_cwd)

        # Create and send an embed with the guild information
        guild_embed = nextcord.Embed(
            title=f"Guild Information - {guild.name}",
            color=nextcord.Color.blue()
        )
        guild_embed.add_field(name="Owner", value=owner, inline=False)
        guild_embed.add_field(name="Member Count", value=member_count, inline=False)
        guild_embed.add_field(name="Text Channels", value=text_channels, inline=False)
        guild_embed.add_field(name="Voice Channels", value=voice_channels, inline=False)
        guild_embed.add_field(name="Roles", value=roles_count, inline=False)

        try:
            await interaction.response.send_message(embed=guild_embed)
        except nextcord.NotFound:
            # Interaction is no longer valid, and responding is not possible
            return

        # Create and send an embed with the system and file information
        system_info = f"Platform: {platform.system()}\n"
        system_info += f"OS: {platform.release()}\n"
        system_info += f"Processor: {platform.processor()}\n"
        system_info += f"Bot Working Directory: {bot_cwd}\n"
        system_info += f"Bot Files and Folders:\n"
        system_info += "\n".join(bot_files)

        system_embed = nextcord.Embed(title="System and File Information", description=system_info, color=nextcord.Color.green())

        try:
            await interaction.followup.send(embed=system_embed)
        except nextcord.NotFound:
            # Interaction is no longer valid, and responding is not possible
            return

def setup(client):
    client.add_cog(Info(client))
                   
