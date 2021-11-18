import json
import uuid
import pytz

from timezone_field.rest_framework import TimeZoneSerializerField
from rest_framework import serializers
from django_celery_beat.models import CrontabSchedule

from myn_utils.rest_framework.fields import LazyChoiceField

from periodic_tasks_api.utils import (
    get_config_by_task_type,
    get_task_type_choices_from_config,
    get_entity_from_path_string,
    get_next_execution_time_from_crontab_string,
    convert_crontab_instance_to_string,
)
from periodic_tasks_api.models import CustomExtendedPeriodicTask


class CronTabSerializer(serializers.ModelSerializer):

    timezone = TimeZoneSerializerField()
    timezone_choices = LazyChoiceField(choices=pytz.all_timezones, read_only=True)

    class Meta:
        model = CrontabSchedule
        fields = '__all__'

    def create(self, validate_data):
        try:
            instance = self.Meta.model.objects.get(**validate_data)
        except self.Meta.model.DoesNotExist:
            return super().create(validate_data)

        if instance:
            return self.update(instance, validate_data)
        return super().create(validate_data)


class PeriodicTaskSerializer(serializers.ModelSerializer):
    task_type = LazyChoiceField(required=True, choices=get_task_type_choices_from_config)

    kwargs = serializers.JSONField(default=dict)

    cron_tab_data = CronTabSerializer(required=False)

    next_execution_time = serializers.SerializerMethodField()

    _nested_serializers = {
        "cron_tab_data": {
            'periodic_task_time_key': 'crontab_id',
            'serializer': CronTabSerializer,
        }
    }

    class Meta:
        model = CustomExtendedPeriodicTask
        fields = (
            'id', 'kwargs', 'enabled', 'description', 'task_type', 'cron_tab_data', 'last_run_at',
            'next_execution_time'
        )
        read_only_fields = ('last_run_at',)

    def get_next_execution_time(self, periodic_task):
        """ return date time string in iso format """
        # TODO extend it for another schedulers
        if not periodic_task.crontab:
            return
        crontab_string = convert_crontab_instance_to_string(periodic_task.crontab)
        return get_next_execution_time_from_crontab_string(
            crontab_string, periodic_task.crontab.timezone
        )

    def validate(self, attrs):
        self.config = get_config_by_task_type(attrs.get("task_type"))

        # Name handle
        task_type = attrs.get("task_type", "")
        attrs["name"] = ' '.join([task_type, str(uuid.uuid4())])

        # Validate kwargs
        kwargs_serializer_path = self.config.get("kwargs_serializer")

        if kwargs_serializer_path:
            kwargs_serializer = get_entity_from_path_string(kwargs_serializer_path)
            kws = kwargs_serializer(data=attrs.get("kwargs"))
            kws.is_valid(raise_exception=True)

        return attrs

    def setup_config_fields(self, instance):
        if not self.config.get("path_to_task"):
            raise serializers.ValidationError({"path_to_task": "Not configured."})

        instance.task = self.config.get("path_to_task")
        instance.queue = self.config.get("queue")
        if not instance.priority:
            instance.priority = self.config.get("priority")

        if self.config.get("additional_kwargs"):
            instance.kwargs.update(self.config.get("additional_kwargs", {}))

        instance.save()
        return instance

    def _pop_nested_serializers_data(self, validated_data):
        nested_serializers_data = {}
        for field in self._nested_serializers.keys():
            if validated_data.get(field):
                nested_serializers_data[field] = validated_data.pop(field)
        return validated_data, nested_serializers_data

    def save_nested_serializers(self, nested_serializers_data):
        # TODO: we can remove this when UI will have access here
        if not nested_serializers_data:
            nested_serializers_data = {"cron_tab_data": self.config.get("cron_tab_data")}

        for key, nested_serializer in self._nested_serializers.items():
            nested_serializer_conf = nested_serializers_data.get(key)

            nested_serializer_class = self._nested_serializers.get(key, {}).get("serializer")
            if not nested_serializer_class:
                continue
            nested_serializer = nested_serializer_class(data=nested_serializer_conf)
            nested_serializer.is_valid()
            nested_serializer.save()
            nested_object_id = nested_serializer.instance.id
            periodic_task_time_id = self._nested_serializers.get(key, {}).get("periodic_task_time_key")
            return {periodic_task_time_id: nested_object_id}

    @staticmethod
    def prepare_kwargs_to_save(kwargs):
        return json.dumps(kwargs)

    def create(self, validated_data):
        validated_data, nested_serializers_data = self._pop_nested_serializers_data(validated_data)
        time_object = self.save_nested_serializers(nested_serializers_data)

        validated_data.update(time_object)

        validated_data["kwargs"] = self.prepare_kwargs_to_save(validated_data.get("kwargs", {}))

        instance = super().create(validated_data)
        instance = self.setup_config_fields(instance)
        return instance

    def update(self, instance, validated_data):
        validated_data, nested_serializers_data = self._pop_nested_serializers_data(validated_data)
        time_object = self.save_nested_serializers(nested_serializers_data)
        validated_data.update(time_object)

        validated_data["kwargs"] = self.prepare_kwargs_to_save(validated_data.get("kwargs", {}))

        instance = super().update(instance, validated_data)
        instance = self.setup_config_fields(instance)
        return instance
