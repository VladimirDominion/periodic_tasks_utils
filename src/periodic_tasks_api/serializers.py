from rest_framework import serializers

from utils import get_config_by_task_type


class PeriodicTaskInputSerializer(serializers.Serializer):  # noqa
    task_type = serializers.ChoiceField(choices=[])

    def __init__(self):
        pass

    get_config_by_task_type()
