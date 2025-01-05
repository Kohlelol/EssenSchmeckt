from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django_apscheduler.models import DjangoJobExecution
from database.models import groupleader

def delete_expired_group_leaders():
    expired_groupleaders = groupleader.objects.filter(expires__lt=datetime.now().date())
    expired_groupleaders.delete()
    print(f'Deleted {expired_groupleaders.count()} expired group leaders.')

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Schedule the job to run daily at midnight
    scheduler.add_job(
        delete_expired_group_leaders,
        trigger=CronTrigger(hour="00", minute="00"),
        id="delete_expired_group_leaders",
        max_instances=1,
        replace_existing=True,
    )
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started!")

    # Clean up old job executions
    def delete_old_job_executions(max_age=604_800):
        DjangoJobExecution.objects.delete_old_job_executions(max_age)

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )