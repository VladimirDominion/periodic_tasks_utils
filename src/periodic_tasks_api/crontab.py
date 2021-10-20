from django_celery_beat.models import CrontabSchedule


def get_crontab_instance(minute, hour, timezone):
    instance, _ = CrontabSchedule.objects.get_or_create(minute=minute, hour=hour, timezone=timezone)
    return instance
