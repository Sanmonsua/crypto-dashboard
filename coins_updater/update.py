from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from coins_updater import api

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(api.update_coins, 'cron', hour=0, minute=0)
    scheduler.start()
