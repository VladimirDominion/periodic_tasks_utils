import json

from django.db.models import F
from django_celery_beat.models import PeriodicTask
from django.conf import settings

from crontab import get_crontab_instance


def get_path_to_the_task() -> str:
    """
    The Name of the Celery Task that Should be Run.
    (Example: "proj.tasks.import_contacts")
    """
    path = getattr(settings, "AUTO_SYNC_TASK_PATH", None)
    if not path:
        raise Exception("Auto sync task doesn't have path")
    return path


def create_periodic_task(minute: int, hour: int, timezone: str, row_id: int):
    try:
        crontab = get_crontab_instance(minute, hour, timezone)
        PeriodicTask.objects.create(
            task=get_path_to_the_task(),
            crontab=crontab,
            name=f"{row_id}-{crontab.id}",
            args=json.dumps([row_id]),
        )
    except Exception as e:
        return {"create_periodic_task": f"{e}"}


def get_periodic_task(row_id):
    return PeriodicTask.objects.filter(args=f"[{row_id}]").values(
        "crontab_id",
        timezone=F("crontab__timezone"),
        hour=F("crontab__hour"),
        minute=F("crontab__minute"),
    )


def delete_periodic_task(row_id, crontab_id):
    PeriodicTask.objects.filter(args=f"[{row_id}]", crontab_id=crontab_id).delete()
