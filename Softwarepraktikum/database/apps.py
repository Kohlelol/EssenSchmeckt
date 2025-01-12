from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import logging
import threading

logger = logging.getLogger(__name__)

scheduler_started = threading.Event()

# class GroupleaderListConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'database'

class DatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database'
    
    def ready(self):
        # Schedule a delayed scheduler start
        if not scheduler_started.is_set():
            logger.info("Scheduling delayed scheduler start.")
            from django.core.signals import request_finished
            from .scheduler import start

            # Connect to the first request or post-migrate signal
            @receiver(connection_created)
            def start_scheduler_once(*args, **kwargs):
                if not scheduler_started.is_set():
                    logger.info("Starting scheduler after first request.")
                    start()
                    scheduler_started.set()


