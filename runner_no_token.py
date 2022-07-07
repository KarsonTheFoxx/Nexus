from disnake.ext import commands
import disnake
from os import listdir, unlink
from json import dump

intents = disnake.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
intents.guilds = True

bot = commands.InteractionBot(intents=intents)

for cog in listdir("cogs/"):
        if cog.endswith(".py"):
            bot.load_extension(f"cogs.{cog[:-3]}")


@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(type=disnake.ActivityType.watching, name="The chats"))
    

    print("ready")      

@bot.event
async def on_guild_join(guild):

    for channel in guild.channels:
        try:
            pass
            break
        except Exception:
            print(f"failed in channel: {channel}")
    
    guild_config = {
        "admin-roles": [],
        "mute": None,
        "welcome": {"enabled":False, "channel":None},
        "log": None,
        "word filter": []
    }
    
    with open(f"config/guilds/{guild.id}.json", "x") as new_guild:
        dump(guild_config, new_guild)  
    emb = disnake.Embed(title="Thank you for using `Nexus`!", description="We at `impossible` are glad you decided to go with us! before you begin make sure to use the `manage` command to set up bot admin roles!")
    for channel in guild.channels:
        try:
            await channel.send(embed=emb)
            break
        except Exception:
            pass


@bot.event
async def on_guild_remove(guild):
    unlink(f"config/guilds/{guild.id}.json")



bot.run("TOKEN")