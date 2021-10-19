from django.conf import settings
from django.core.exceptions import ValidationError


def get_periodic_tasks_config() -> list:
    conf = getattr(settings, "PERIODIC_API_CONFIG", None)
    if not conf:
        raise ValidationError("Periodic task utils doesn't have settings for tasks")
    return conf


def get_config_by_task_type(task_type):
    for task_config in get_periodic_tasks_config():
        if task_config["task_type"] == task_type:
            return task_config
