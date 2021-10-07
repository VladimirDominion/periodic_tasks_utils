from django.db.models import F
from django_celery_beat.models import CrontabSchedule, PeriodicTask


def get_path_to_the_task() -> str:
    """
    The Name of the Celery Task that Should be Run.
    (Example: "proj.tasks.import_contacts")
    """
    raise NotImplementedError


def get_task_args() -> list:
    return []


def get_task_kwargs() -> dict:
    return {}


def create_periodic_task(crontab: CrontabSchedule, row_id: int):
    try:
        PeriodicTask.objects.create(
            task=get_path_to_the_task(),
            crontab=crontab,
            name=f"{row_id}-{crontab.id}",
            args=get_task_args(),
            kwargs=get_task_kwargs(),
        )
    except Exception as e:
        return {"create_periodic_task": f"{e}"}


def get_periodic_task(row_id):
    return (
        PeriodicTask.objects.filter(name__startswith=row_id)
        .select_related("crontab")
        .values(
            "name",
            "crontab_id",
            timezone=F("crontab__timezone"),
            hour=F("crontab__hour"),
            minute=F("crontab__minute"),
        )
    )


def delete_periodic_task(task_name):
    PeriodicTask.objects.filter(name=task_name).delete()
