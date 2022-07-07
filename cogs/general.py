from disnake.ext import commands
import disnake
from datetime import datetime

class general_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description="Displays stats about the bot")
    async def stats(self, inter):
        emb = disnake.Embed(title="Stats about Nexus", description="Nexus is open source on github'\nInvite me! Invite me:https://discord.com/api/oauth2/authorize?client_id=993693318510821540&permissions=8&scope=bot%20applications.commands", color=disnake.Color.brand_red())
        emb.add_field(name="Bots creation date", value="Thurs july 2 2022")
        emb.add_field(name="Ping", value=f"{round(self.bot.latency*100, 2)}ms")
        emb.add_field(name="guilds", value=len(self.bot.guilds))

        await inter.response.send_message(embed=emb)

    @commands.slash_command(description="Displays basic information about a user")
    async def whois(self, inter, member:disnake.Member):
        now = datetime.now().strftime("%b %m %y")

        now = datetime.strptime(now, "%b %m %y")

        joined_at = member.joined_at.strftime("%b %m %y")
        joined_at =  datetime.strptime(joined_at, "%b %m %y")

        joined_ago = now - joined_at

        if joined_ago.days < 1:
            timedelta = "less than a day ago"
        else:
            timedelta = f"{joined_ago.days} days ago"

        emb = disnake.Embed(title=f"Information about: {member}")
        emb.add_field(name="joined", value=timedelta)
        emb.add_field(name="id", value=member.id)
        
        roles = ""

        for role in member.roles:
            if member.roles.index(role) != member.roles[-1]:
                roles += f"`{role.name}`, "
            else:
                roles += f"`{role.name}"
        
        emb.add_field(name="roles", value=roles)

        await inter.response.send_message(embed=emb)


def setup(bot):
    bot.add_cog(general_cog(bot))