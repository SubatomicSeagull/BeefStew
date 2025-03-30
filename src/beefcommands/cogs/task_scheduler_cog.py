import discord
import asyncio
from discord.ext import commands, tasks
import datetime
from data import postgres
import random
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
    async def scheduled_holiday_check(self):
        await holiday_check.check_for_holiday(self.bot)
    
    # task is scheduled to check for IOTD every day at 9am
    @tasks.loop(time=datetime.time(9, 0, 0, tzinfo=TIMEZONE))
    async def image_of_the_day_check(self):
        await image_of_the_day.image_of_the_day(self.bot)
        return


    
    @tasks.loop(hours=24)
    async def random_swing_check(self):
        swing_times = [8, 12, 16, 20]  # 8am, 12pm, 4pm, 8pm
        for hour in swing_times:
            
            # add a random number of minutes to the hour
            random_minutes = random.randint(0, 59)
            swing_time = datetime.time(hour, random_minutes, tzinfo=self.TIMEZONE)
            now = datetime.datetime.now(tz=self.TIMEZONE).time()
            print(f"Checking for swing at {swing_time} against {now}")
            # check if the current time matches the swing time
            if now.hour != swing_time.hour and now.minute != swing_time.minute:
                # 1/100 chance for the swing to happen
                if random.randint(1, 100) != 1:
                    
                    # determine the type of swing
                    swing_type = random.choice(["insult", "neutral", "image"])
                    
                    # determine the channel type
                    channel_type = random.choices(["info_channel", "dm"], weights=[1, 2])[0]

                    # read flagged users from the db
                    flagged_users = await postgres.read(f"SELECT user_id FROM users WHERE msg_flag = TRUE;")
                    if not flagged_users:
                        return
                    print(f"Flagged users: {flagged_users}")
                    
                    # pick a random user
                    user_id = random.choice(flagged_users)
                    
                    print(f"Swinging at user {user_id} with type {swing_type} in {channel_type}")

async def setup(bot):
    print("- \033[95mbeefcommands.cogs.task_scheduler_cog\033[0m")
    await bot.add_cog(TaskSchedulerCog(bot))
