import discord
from discord.ext import commands, tasks
import datetime
import beefutilities
import beefutilities.guilds.text_channel
testtime = datetime.time(hour=8, minute=58, tzinfo=datetime.timezone.utc)

class TaskSchedulerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"scheduling tasks...")
        self.test_task.start()
        print(f"\033[32mall tasks scheduled successfully!\033[0m")
       
    @tasks.loop(time=testtime)
    async def test_task(self):
        print(f"{testtime} scheduled task ran at", datetime.datetime.now())
 
        
        

    async def schedule_birthday(self, user:discord.User, birthday):
        # birthdy is currently an argument but will be defined locally as read from the db and converted to a datetime.
        # task is scheduled to read the db every day to check for matching birthdays
        # if there are any, list the users and run the below logic
        
        # schedule a task to run at the datetime value of the users bday
        channel = beefutilities.guilds.text_channel.read_guild_info_channel(self.bot.guild.id)
        await channel.send(f"Happy Birthday {user.mention}!")
        # add a custom imaghe to send along with it
        #add 20 points to the users score

        # actaully all yearly tasks will need to be scheduled this way as there is no support for yearly tasks in discord.ext for some reason

        
async def setup(bot):
    print("- \033[95mbeefcommands.cogs.task_scheduler_cog\033[0m")
    await bot.add_cog(TaskSchedulerCog(bot))