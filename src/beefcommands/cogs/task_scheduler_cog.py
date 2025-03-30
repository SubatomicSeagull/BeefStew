import discord
from discord.ext import commands, tasks
import datetime
from zoneinfo import ZoneInfo
from beefcommands.events.tasks import holiday_check, birthday_check, image_of_the_day
class TaskSchedulerCog(commands.Cog):
    
    TIMEZONE = ZoneInfo("Europe/London")
    
    def __init__(self, bot):
        self.bot = bot
        print(f"> Timezone set to {self.TIMEZONE}")
        print(f"> Scheduling Tasks...")
        self.scheduled_birthday_check.start()
        self.scheduled_holiday_check.start()
        print(f"\033[32mall tasks scheduled successfully!\033[0m")
    
    # task is scheduled to check for birthdays every day at 10am
    @tasks.loop(time=datetime.time(10, 0, 0, tzinfo=TIMEZONE))
    async def scheduled_birthday_check(self):
        await birthday_check.check_for_birthdays(self.bot)
    
    # task is scheduled to check for holidays every day at 8am
    @tasks.loop(time=datetime.time(8, 0, 0, tzinfo=TIMEZONE))
    async def scheduled_holiday_check(self, ctx):
        await holiday_check.check_for_holiday(self.bot)
    
    # task is scheduled to check for IOTD every day at 9am
    #@tasks.loop(time=datetime.time(9, 0, 0, tzinfo=TIMEZONE))
    @commands.command(name="iotd")  
    async def image_of_the_day_check(self, ctx):
        await image_of_the_day.image_of_the_day(self.bot)
        return
        
    async def random_swing_check(self):
        pass
        # if a user has the msg flag you get from being sniffed, they will be eligable for a random swing
        # a random swing event has a chance to happen 4 times a day, 8am, 12om, 4pm and 8pm
        # there is a low chance of a swing happeneing at one of these times, like 1/100
        # of this 1 in 100 chance, 1/3 chance to be an insult from, 1/3 chance to be neutral, 1/3 chance to be an image (swing responses in responses.json)
        # also of this 1 in 100 chance, there is a 1/3 chance for it to be in the info channel, and 2/3 chance for it to be a DM.
        
        # at one of the 4 times, all the flagged users will be gathered and one will be picked at random
        # 1/100 check for the swing to happen, then check for type, and then check for channel
        # send the message to the channel or user

        
async def setup(bot):
    print("- \033[95mbeefcommands.cogs.task_scheduler_cog\033[0m")
    await bot.add_cog(TaskSchedulerCog(bot))
    