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

        
    async def scheduled_yearly_event_check(self):
        pass
        # task is scheduled to check for yearly events every day, for some reason theres no way to schedule yearly tasks??
        # calls checks for birthdays and holidays

    async def scheduled_birthday_check(self):
        pass
        # birthdy is currently an argument but will be defined locally as read from the db and converted to a datetime.
        # task is scheduled to read the db every day to check for matching birthdays
        # if there is a match, the bot will send a message to the info channel adn give them 15 points
        
    async def scheduled_holiday_check(self):
        pass
        # task is scheduled to check for holidays every day
        # currently christmas (25/12), new years (1/1) and halloween (31/10)
        # if there is a match, the bot will send a message to the info channel and differing amounts of points
        
    async def image_of_the_day_check(self):
        pass
        # take the current date and match against the list of IOTD's
        # if there is a match, send the image to the info channel
        
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