from disnake.ext import commands
import disnake

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="See help menu")
    async def help(self, inter):

        moderation = disnake.Embed(title="Moderation commands", description="Any moderator roles can use these commands\n <arg> = required\n[arg] = optional", color=disnake.Color.orange())
        moderation.add_field(name="mute", value="Mutes a user for a specified amount of time.\n*Syntax:* `mute <user> <int: duration> <mode: seconds, minutes, etc> [reason]`", inline=False)
        moderation.add_field(name="Kick", value="Kicks a user frim the guild\n*Syntax:*`kick <user> [reason]`", inline=False)
        moderation.add_field(name="Ban", value="Bans a user from the guild\n*Syntax:*`ban <user> [reason]`", inline=False)

        manage = disnake.Embed(title="Manage commands", description="Commands to manage the configuration of the bot in the current guild, ONLY GUILD OWNERS CAN RUN THIS COMMAND!\n all commands here are prefixed with `/manage`\n <arg> = required\n[arg] = optional", color=disnake.Color.dark_gold())
        manage.add_field(name="admin-role", value="Manages bot admin roles\n*Syntax:*`admin-role <add/remove> <role>")
        manage.add_field(name="set-welcome", value="Sets the welcome channel\n*Syntax:*`set-welcome <text channel>`")
        manage.add_field(name="toggle-welcome", value="Toggle the join message on user join\n*Syntax:*`toggle-welcome`")
        manage.add_field(name="mute-role", value="Sets the role to be given when a user is muted\n*Syntax:*`mute-role <role>`")

        general = disnake.Embed(title="General commands", description="General commands for everyone\n <arg> = required\n[arg] = optional", color=disnake.Color.fuchsia())
        general.add_field(name="WhoIs", value="Displays basic information about a user\n*Syntax:*`whois <user>`")
        general.add_field(name="help", value="Display this menu\n*Syntax:*`help [command group]")
        general.add_field(name="stats", value="Displays bot stats")

        basic = disnake.Embed(title="Help menu", description="This help menu will show you how to use the basic commands of the bot, if you are struggling you can join our support server.\nhttps://discord.gg/bXHm3x6aky")

        embeds = {"general":general, "moderation":moderation, "manage":manage}

        view = disnake.ui.View(timeout=15)

        menu = disnake.ui.Select(options=[
            disnake.SelectOption(label="General",description="General commands"),
            disnake.SelectOption(label="Moderation", description="Moderation commands"),
            disnake.SelectOption(label="Manage", description="Manage commands")
        ],
        min_values=1, max_values=1)
        view.add_item(menu)

        await inter.response.send_message(embed=basic, view=view)
        async def callback(minter:disnake.MessageInteraction):
            if inter.author == minter.author:
                await minter.response.defer(with_message=False)
                item = minter.values[0].lower()

                current_emb = embeds[item]
                await inter.edit_original_message(embed=current_emb, view=view)
            
            else:
                await minter.response.send_message("This menu isnt yours!", ephemeral=True)

        
        menu.callback = callback


def setup(bot):
    bot.add_cog(help_cog(bot))