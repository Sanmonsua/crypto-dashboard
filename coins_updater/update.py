from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from coins_updater import api

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(api.update_coins, 'interval', hours=8)
    scheduler.start()
