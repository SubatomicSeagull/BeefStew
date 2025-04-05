import discord
import asyncio
from discord.ext import commands, tasks
import datetime
from data import postgres
import random
from zoneinfo import ZoneInfo
from beefcommands.events.tasks import holiday_check, birthday_check, image_of_the_day, random_swing
class TaskSchedulerCog(commands.Cog):
    
    TIMEZONE = ZoneInfo("Europe/London")
    
    def __init__(self, bot):
        self.bot = bot
        print(f"> Timezone set to {self.TIMEZONE}")
        print(f"> Scheduling Tasks...")
        self.scheduled_birthday_check.start()
        self.scheduled_holiday_check.start()
        self.image_of_the_day_check.start()
        self.random_swing_check.start()
        print(f"\033[32mall tasks scheduled successfully!\033[0m")
    
    # task is scheduled to check for birthdays every day at 10am
    @tasks.loop(time=datetime.time(10, 0, 0, tzinfo=TIMEZONE))
    async def scheduled_birthday_check(self):
        await birthday_check.check_for_birthdays(self.bot)
    
    # task is scheduled to check for holidays every day at 8am
    @tasks.loop(time=datetime.time(8, 0, 0, tzinfo=TIMEZONE))
    async def scheduled_holiday_check(self):
        await holiday_check.check_for_holiday(self.bot)
    
    # task is scheduled to check for IOTD every day at 9am
    @tasks.loop(time=datetime.time(9, 0, 0, tzinfo=TIMEZONE))
    async def image_of_the_day_check(self):
        await image_of_the_day.image_of_the_day(self.bot)
        return

    @tasks.loop(time=[
        datetime.time(hour=8, tzinfo=TIMEZONE),
        datetime.time(hour=12, tzinfo=TIMEZONE),
        datetime.time(hour=18, tzinfo=TIMEZONE),
        datetime.time(hour=22, tzinfo=TIMEZONE)
    ])
    async def random_swing_check(self):
        await random_swing.random_swing_check(self.bot)

async def setup(bot):
    print("- \033[95mbeefcommands.cogs.task_scheduler_cog\033[0m")
    await bot.add_cog(TaskSchedulerCog(bot))
