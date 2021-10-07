from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AutoSyncInputSerializer,
    AutoSyncRetrieveSerializer,
    AutoSyncDeleteSerializer,
)
from .crontab import get_crontab_instance
from .periodic_task import create_periodic_task, get_periodic_task, delete_periodic_task


class AutoSyncView(APIView):
    def get(self, request):
        row_id = request.query_params.get("row_id")
        if not row_id:
            raise ValidationError("Url must contain 'row_id' param")
        queryset = get_periodic_task(row_id)
        serializer = AutoSyncRetrieveSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    def post(self, request):
        serializer = AutoSyncInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        crontab = get_crontab_instance(
            hour=validated_data["hour"], minute=validated_data["minute"], timezone=validated_data["timezone"]
        )
        error = create_periodic_task(crontab=crontab, row_id=validated_data["row_id"])
        return Response({"error": error})

    def delete(self, request):
        serializer = AutoSyncDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delete_periodic_task(**serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
