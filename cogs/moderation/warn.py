import nextcord
from nextcord.ext import commands
import json

class Warn(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.warn_data = {}  # We will use this to store warnings

    def save_warn_data(self):
        with open('warn_data.json', 'w') as f:
            json.dump(self.warn_data, f, indent=4)

    def load_warn_data(self):
        try:
            with open('warn_data.json', 'r') as f:
                self.warn_data = json.load(f)
        except FileNotFoundError:
            self.warn_data = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.load_warn_data()

    @nextcord.slash_command()
    @commands.has_permissions(ban_members=True)
    async def warn(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason="No reason provided"):
        if interaction.user == member:
            return await interaction.response.send_message("You cannot warn yourself!")

        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message("You cannot warn a member with equal or higher role!")

        if str(interaction.guild.id) not in self.warn_data:
            self.warn_data[str(interaction.guild.id)] = {}

        if str(member.id) not in self.warn_data[str(interaction.guild.id)]:
            self.warn_data[str(interaction.guild.id)][str(member.id)] = []

        self.warn_data[str(interaction.guild.id)][str(member.id)].append(reason)
        self.save_warn_data()

        embed = nextcord.Embed(title=f"Member Warned: {member.name}", color=nextcord.Color.orange())
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command()
    async def warnings(self, interaction: nextcord.Interaction, member: nextcord.Member):
        if str(interaction.guild.id) not in self.warn_data or str(member.id) not in self.warn_data[str(interaction.guild.id)]:
            return await interaction.response.send_message("No warnings found for this member!")

        warnings = self.warn_data[str(interaction.guild.id)][str(member.id)]
        embed = nextcord.Embed(title=f"Warnings for {member.name}", color=nextcord.Color.red())
        for idx, warning in enumerate(warnings, start=1):
            embed.add_field(name=f"Warning {idx}", value=warning, inline=False)

        await interaction.response.send_message(embed=embed)

def setup(client):
    client.add_cog(Warn(client))
