from discord.ext import commands, tasks
import datetime
from zoneinfo import ZoneInfo
from beefcommands.events.tasks import cleanup_tts, holiday_check, birthday_check, image_of_the_day, random_swing
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
        self.clean_temp_tts_files.start()
        print(f"\033[32mall tasks scheduled successfully!\033[0m")

    # task to clean out any old temp tts files that might have been left every day at midnight
    @tasks.loop(time=datetime.time(0, 0, 0, tzinfo=TIMEZONE))
    async def clean_temp_tts_files(self):
        await cleanup_tts.cleanup_tts_folder()

    # task is scheduled to check for birthdays every day at 10am
    @tasks.loop(time=datetime.time(9, 3, 0, tzinfo=TIMEZONE))
    async def scheduled_birthday_check(self):
        await birthday_check.check_for_birthdays(self.bot)

    # task is scheduled to check for holidays every day at 8am
    @tasks.loop(time=datetime.time(9, 34, 0, tzinfo=TIMEZONE))
    async def scheduled_holiday_check(self):
        await holiday_check.check_for_holiday(self.bot)

    # task is scheduled to check for IOTD every day at 9am
    @tasks.loop(time=datetime.time(9, 5, 0, tzinfo=TIMEZONE))
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
