from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


async def update_meal():
    return


def setup(scheduler: AsyncIOScheduler):
    cron_trigger = CronTrigger(day_of_week=1)
    scheduler.add_job(update_meal, trigger=cron_trigger)
