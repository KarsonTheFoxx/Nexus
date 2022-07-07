from disnake.ext import commands
import disnake
import json
from datetime import timedelta, datetime, date

class welcome_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member:disnake.Member):
        guild = member.guild

        joined_at = member.joined_at.strftime("%b %m %y")
        created_at = member.created_at.strftime("%b %m %y")

        joined_after = datetime.strptime(joined_at, "%b %m %y") -  datetime.strptime(created_at, "%b %m %y")
        
        emb = disnake.Embed(title=f"Welcome `{member}`!", color=disnake.Color.green())
        emb.add_field(name="Joined Date", value=f"`{joined_at}`", inline=True)
        emb.add_field(name="Creation Date", value=f"`{created_at}`", inline=True)
        emb.add_field("Joined guild after", value=f"`{joined_after.days}` days after account creation", inline=False)

        with open(f"config/guilds/{guild.id}.json") as GCF:
            GC = json.load(GCF)
        
        if GC["log"] != None:
            channel = disnake.utils.get(guild.channels, id=GC["welcome"]["channel"])

            await channel.send(content=member.mention, embed=emb)

def setup(bot):
    bot.add_cog(welcome_cog(bot))