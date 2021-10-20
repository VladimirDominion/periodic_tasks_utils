from django_celery_beat.schedulers import DatabaseScheduler

from periodic_tasks_api.models import CustomExtendedPeriodicTask


class CustomDatabaseScheduler(DatabaseScheduler):
    Model = CustomExtendedPeriodicTask
