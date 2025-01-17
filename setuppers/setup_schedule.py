import schedule
import time

def setup_schedule(job, logger):
    schedule.every(5).minutes.do(lambda: job(logger))
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)