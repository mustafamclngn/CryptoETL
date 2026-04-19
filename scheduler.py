from apscheduler.schedulers.blocking import BlockingScheduler
from pipeline import run_pipeline

scheduler = BlockingScheduler()
scheduler.add_job(run_pipeline, "interval", minutes=10)

# ctrl + c stop
print("SCHEDULER RUNNING - 10 MINUTE INTERVAL")

run_pipeline()      # run once immediately on start
scheduler.start()