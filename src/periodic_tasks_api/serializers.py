from rest_framework import serializers


class AutoSyncInputSerializer(serializers.Serializer):  # noqa
    row_id = serializers.IntegerField()
    hour = serializers.IntegerField(min_value=0, max_value=23)
    minute = serializers.IntegerField(min_value=0, max_value=59)
    timezone = serializers.CharField(default="UTC")


class AutoSyncRetrieveSerializer(serializers.Serializer):  # noqa
    crontab_id = serializers.IntegerField()
    timezone = serializers.CharField()
    hour = serializers.IntegerField()
    minute = serializers.IntegerField()


class AutoSyncDeleteSerializer(serializers.Serializer):  # noqa
    row_id = serializers.IntegerField()
    crontab_id = serializers.IntegerField()
