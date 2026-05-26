from app.gatekeeper import sync_blocked_sites
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def register_jobs():

    scheduler.add_job(sync_blocked_sites, trigger="cron", hour=0, minute=0)
