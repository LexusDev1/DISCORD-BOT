import nextcord
from nextcord.ext import commands
from nextcord.ui import View, button

class BanButton(View):
    def __init__(self, member: nextcord.Member):
        super().__init__()
        self.value = None
        self.member = member

    @button(label="ConfirmBan", style=nextcord.ButtonStyle.red)
    async def confirmkick(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"Banning {self.member.display_name}...")
        await self.member.ban(reason="Ban requested by moderator.")
        await interaction.followup.send(f"{self.member.display_name} has been ban.")

class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, member: nextcord.Member):
        view = KickButton(member)
        embed = nextcord.Embed(description=f"Are you sure you want to ban {member.display_name}?")
        await interaction.response.send_message(embed=embed, view=view)

def setup(client):
    client.add_cog(Ban(client))
    