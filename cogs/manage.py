from disnake.ext import commands
import disnake
import json


class manage_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="manage", description="Manage guild properties")
    async def manage(self, inter):
        pass

    @manage.sub_command(name="mute-role", description="Changes the mute role")
    async def mute_role(self, inter, role:disnake.Role):
        with open("config/global/config.json", "r") as GC:
            GLC = json.load(GC)
        
        with open(f"config/guilds/{inter.guild.id}.json", "r") as GCF:
            GC = json.load(GCF)
        
        if inter.author.id in GLC["command-banned"] or not inter.author.id == inter.guild.owner.id:
            await inter.response.send_message(f"Only {inter.guild.owner} can run this command!")

        else:
            GC["mute"] = role.id

            with open(f"config/guilds/{inter.guild.id}.json", "w") as GCN:
                json.dump(GC, GCN)
            
            await inter.response.send_message("The mute role has been updated")
    
    @manage.sub_command_group(name="admin-role", description="Manage bot admin roles")
    async def admin_roles(self, inter):
        pass

    @admin_roles.sub_command(name="add", description="Add an admin role")
    async def add_admin(self, inter, role:disnake.Role):
        with open("config/global/config.json", "r") as GC:
            GLC = json.load(GC)
    
        with open(f"config/guilds/{inter.guild.id}.json", "r") as GCF:
            GC = json.load(GCF)

        if inter.author.id in GLC["command-banned"] or not inter.author.id == inter.guild.owner.id:
            await inter.response.send_message(f"Only {inter.guild.owner} can run this command!")
        else:
            if role.id not in GC["admin-roles"]:
                GC["admin-roles"].append(role.id)
                with open(f"config/guilds/{inter.guild.id}.json", "w") as GCN:
                    json.dump(GC, GCN)
                
                await inter.response.send_message("Role added")
            else:
                await inter.response.send_message("That role is already a moderator")

    @admin_roles.sub_command(name="remove", description="Remove an admin role")
    async def remove_admin(self, inter, role:disnake.Role):
        with open("config/global/config.json", "r") as GC:
            GLC = json.load(GC)
    
        with open(f"config/guilds/{inter.guild.id}.json", "r") as GCF:
            GC = json.load(GCF)
        
        await inter.response.send_message("Role removed")

        if inter.author.id in GLC["command-banned"] or not inter.author.id == inter.guild.owner.id:
            await inter.response.send_message(f"Only {inter.guild.owner} can run this command!")
        else:
        
            for roleid in GC["admin-roles"]:
                if roleid == role.id:
                    GC["admin-roles"].remove(roleid)
                    with open(f"config/guilds/{inter.guild.id}.json", "w") as GCN:
                        json.dump(GC, GCN)
            
            await inter.response.send_message("Moderators have been updated")
            
    @manage.sub_command(name="log-channel", description="Sets the log channel")
    async def log_channel(self, inter, channel:disnake.TextChannel):
        with open("config/global/config.json", "r") as GC:
            GLC = json.load(GC)
    
        with open(f"config/guilds/{inter.guild.id}.json", "r") as GCF:
            GC = json.load(GCF)

        if inter.author.id in GLC["command-banned"] or not inter.author.id == inter.guild.owner.id:
            await inter.response.send_message(f"Only {inter.guild.owner} can run this command!")
        else:  
            GC["log"] = channel.id
            with open(f"config/guilds/{inter.guild.id}.json", "w") as GCN:
                json.dump(GC, GCN)

                await inter.response.send_message("Log channel set")
        
    @manage.sub_command(name="toggle-welcome", description="Toggle the welcome message on and off")
    async def toggle_welcome(self, inter):
        with open("config/global/config.json", "r") as GC:
            GLC = json.load(GC)
    
        with open(f"config/guilds/{inter.guild.id}.json", "r") as GCF:
            GC = json.load(GCF)

        if inter.author.id in GLC["command-banned"] or not inter.author.id == inter.guild.owner.id:
            await inter.response.send_message(f"Only {inter.guild.owner} can run this command!")   

        else:
            GC["welcome"]["enabled"] = not GC["welcome"]["enabled"]
            await inter.response.send_message(f"welcome set to {GC['welcome']['enabled']}")
            with open(f"config/guilds/{inter.guild.id}.json", "w") as GCN:
                json.dump(GC, GCN)

    @manage.sub_command(name="set-welcome", description="Sets the welcome channel")
    async def set_welcome(self, inter, channel:disnake.TextChannel):
        with open("config/global/config.json", "r") as GC:
            GLC = json.load(GC)
    
        with open(f"config/guilds/{inter.guild.id}.json", "r") as GCF:
            GC = json.load(GCF)

        if inter.author.id in GLC["command-banned"] or not inter.author.id == inter.guild.owner.id:
            await inter.response.send_message(f"Only {inter.guild.owner} can run this command!") 
        
        else:
            GC["welcome"]["channel"] = channel.id

            with open(f"config/guilds/{inter.guild.id}.json", "w") as GCN:
                json.dump(GC, GCN)
            
            await inter.response.send_message("The welcome channel has been set")

def setup(bot):
    bot.add_cog(manage_cog(bot))