import logging

from django.db.models import F
from django.db.models.functions import Cast
from django.contrib.postgres.fields import JSONField
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask

from periodic_tasks_api.serializers import PeriodicTaskSerializer

from periodic_tasks_api.utils import get_config_by_task_type, get_entity_from_path_string


class Command(BaseCommand):

    task_type = "auto-sync"

    def handle(self, *args, **options):
        logging.basicConfig()

        config = get_config_by_task_type(self.task_type)
        command_model = get_entity_from_path_string(config.get("command_model"))
        command_field_key = config.get("command_field_key")
        row_ids = command_model.objects.values_list(command_field_key,flat=True).distinct()

        created_rows = []
        existed_rows = []
        for row_id in row_ids:
            periodic_task = (
                PeriodicTask.objects.all()
                .annotate(jkwargs=Cast(F('kwargs'), JSONField()))
                .filter(jkwargs__row_id=str(row_id))
            )
            if periodic_task:
                existed_rows.append(row_id)
                continue

            serializer = PeriodicTaskSerializer(
                data={
                    "kwargs": {"row_id": str(row_id)},
                    "enabled": True,
                    "task_type": self.task_type,
                }
            )
            serializer.is_valid()
            serializer.save()
            created_rows.append(row_id)

        logging.info("Created {} tasks for. Already exist {} tasks.".format(len(created_rows), len(existed_rows)))
