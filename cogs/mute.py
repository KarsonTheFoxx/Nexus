from disnake.ext import commands
import disnake
import json
from datetime import datetime
from asyncio import sleep


class mute_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description="Mutes a user for a specified duration")
    async def mute(self, inter, member:disnake.Member, duration:int, mode:str=commands.Param(choices=["Seconds", "Minutes", "Hours", "Days", "Weeks"]), reason:str="No reason"):

        with open("config/global/config.json", "r") as GLCF:
            GLC = json.load(GLCF)
        
        with open(f"config/guilds/{inter.guild.id}.json", "r") as GCF:
            GC = json.load(GCF)
        
        admin = False
        for role_id in GC["admin-roles"]:
            role = disnake.utils.get(inter.guild.roles, id=role_id)
            if role in inter.author.roles:
                admin = True
                break
        
        if inter.author.id not in GLC["command-banned"] and admin:
            await inter.response.defer()
            
            mode = mode.lower()
            if mode == "minutes":
                duration *= 60
            
            if mode == "hours":
                duration *= 3600
            
            if mode == "days":
                durtion *= 86400
            
            if mode == "weeks":
                duration *= 604800

            if GC["mute"] != None:
                if GC["log"] != None:
                    channel = disnake.utils.get(inter.guild.channels, id=GC["log"])
                    emb = disnake.Embed(title="User muted", description=f"{member} was muted by {inter.author}", color=disnake.Color.red())
                    emb.add_field(name="moderator", value=inter.author)
                    emb.add_field(name="user", value=member)
                    emb.add_field(name="time", value=datetime.now().strftime("%b %m %y"))
                    emb.add_field(name="reason", value=reason)
                    await channel.send(embed=emb)

                await inter.channel.send("User muted")


                role = disnake.utils.get(inter.guild.roles, id=GC["mute"])
                await member.add_roles(role)
                await member.add_roles(role)
                await member.send(f"You have been muted in {inter.guild}, i will notify you when you can talk again!")
                await sleep(duration)
                await member.remove_roles(role)
                await member.send(f"You have been unmuted in {inter.guild}")
            

        else:
            await inter.response.send_message("You may not use this command!")

    @mute.error
    async def on_mute_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Command Failed! i dont have permission to do that!")
        
        else:
            await ctx.send("An unknown error has happened please try again later")
            print(error)

def setup(bot):
    bot.add_cog(mute_cog(bot))