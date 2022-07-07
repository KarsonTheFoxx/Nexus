from disnake.ext import commands
import disnake
import json
from datetime import datetime

class ban_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description="Bans a member from the guild")
    async def ban(self, inter, member:disnake.Member, reason:str="No reason"):

        with open("config/global/config.json", "r") as GC:
            GLC = json.load(GC)
        
        with open(f"config/guilds/{inter.guild.id}.json", "r") as GCF:
            GC = json.load(GCF)

        for role_id in GC["admin-roles"]:
            role = disnake.utils.get(inter.guild.roles, id=role_id)
            if role in inter.author.roles:
                admin = True
                break
            else:
                admin = False
        
        if inter.author.id not in GLC["command-banned"] and admin:
            await member.ban(reason=reason)
            await inter.response.send_message(f"The use {member} was kicked by {inter.author} for {reason}\nLogging this action")

            if GC["log"] != None:
                log_channel = disnake.utils.get(inter.guild.channels, id=GC["log"])
                
                await log_channel.send(f"User: `{member} was banned by {inter.author} for {reason} on {datetime.now().strftime('%a %d %b %Y')}")
    
        else:
            await inter.response.send_message("You may not use this command!")
            
def setup(bot):
    bot.add_cog(ban_cog(bot))