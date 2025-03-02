import discord
from discord.ext import commands, tasks
import beefutilities
import beefutilities.guilds

class TaskSchedulerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def schedule_birthday(self, user:discord.User, birthday):
        # birthdy is currently an argument but will be defined locally as read from the db.
        # birthday event isnt scheduled for users who havent regisered or dont have a bday.
        # event is scheduled when they register a bday using /birthday
        
        # schedule a task to run at the datetime value of the users bday
        await discord.utils.sleep_until(birthday)
        channel = beefutilities.guilds.read_guild_info_channel(self.bot.guild.id)
        await channel.send(f"Happy Birthday {user.mention}!")
        # add a custom imaghe to send along with it
        #add 20 points to the users score
        
        
    async def schedule_christmas(self):
        # schedule a task to run at the datetime value of christmas day
        await discord.utils.sleep_until("12/25")
        channel = beefutilities.guilds.read_guild_info_channel(self.bot.guild.id)
        await channel.send(f"Merry Christmas! What did ol' St. Stew get u huh?\n +10 to everyone :)")
        # add a custom image to send along with it
        # add 10 points to each users score
        
    async def schedule_halloween(self):
        # schedule a task to run at the datetime value of christmas day
        await discord.utils.sleep_until("10/31")
        channel = beefutilities.guilds.read_guild_info_channel(self.bot.guild.id)
        await channel.send(f"ooooOOOoooo! Happy Halloween!! Trick or Treat? fine.. heres some candy.\n +5 to everyone")
        # add a custom image to send along with it
        # add 5 points to each users score
        
        
        
def setup(bot):
    print("- \033[95mbeefcommands.cogs.task_scheduler_cog\033[0m")
    bot.add_cog(TaskSchedulerCog(bot))