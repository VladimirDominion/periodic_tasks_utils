from datetime import datetime

from django.core.exceptions import ValidationError
from django_celery_beat.models import PeriodicTask


def generate_task_name(task_type):
    return f"{task_type}:{datetime.now().timestamp()}"


def create_periodic_task(task_type, **kwargs):
    try:
        name = generate_task_name(task_type)
        PeriodicTask.objects.create(name=name, description=task_type, **kwargs)
    except ValidationError as e:
        return {"create_periodic_task": f"{e}"}


def get_periodic_task(**kwargs):
    return PeriodicTask.objects.filter(**kwargs)
