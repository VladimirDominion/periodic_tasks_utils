from django.db import models
from django_celery_beat.models import PeriodicTask


class CustomExtendedPeriodicTask(PeriodicTask):
    task_type = models.CharField(null=True, blank=True, max_length=100)
