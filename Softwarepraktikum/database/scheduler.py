from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django_apscheduler.models import DjangoJobExecution
from database.models import groupleader, PDFDocument
import os


scheduler_started = False


def delete_expired_group_leaders():
    expired_groupleaders = groupleader.objects.filter(expires__lt=datetime.now().date())
    expired_groupleaders.delete()
    print(f'Deleted {expired_groupleaders.count()} expired group leaders.')

def delete_expired_pdfs():
    expired_pdfs = PDFDocument.objects.filter(expire_date__lt=datetime.now().date())
    for pdf in expired_pdfs:
        if os.path.isfile(pdf.file.path):
            os.remove(pdf.file.path)
        pdf.delete()
    print(f'Deleted {expired_pdfs.count()} expired PDF files.')


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def start():
    global scheduler_started
    if not scheduler_started:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_expired_group_leaders,
            trigger=CronTrigger(hour="00", minute="00"),
            id="delete_expired_group_leaders",
            max_instances=1,
            replace_existing=True,
        )
        
        scheduler.add_job(
            delete_expired_pdfs,
            trigger=CronTrigger(hour="00", minute="00"),
            id="delete_expired_pdfs",
            max_instances=1,
            replace_existing=True,
        )
        
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
    
        register_events(scheduler)
        scheduler.start()
        scheduler_started = True
        delete_expired_group_leaders()
        delete_expired_pdfs()
        print("Scheduler started!")
    
    # delete_expired_group_leaders()
    # delete_expired_pdfs()
    
