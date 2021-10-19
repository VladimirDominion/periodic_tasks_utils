from django.db.models import F
from django.db.models.functions import Cast
from django.contrib.postgres.fields import JSONField

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from periodic_tasks_api.models import CustomExtendedPeriodicTask
from periodic_tasks_api.serializers import PeriodicTaskSerializer


class PeriodicTaskView(viewsets.ModelViewSet):
    queryset = CustomExtendedPeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        row_id = self.request.GET.get('row_id')
        if row_id:
            try:
                row_id = int(row_id)
            except ValueError:
                raise ValidationError({"row_id": "wrong value."})
            queryset = queryset.annotate(json=Cast(F('kwargs'), JSONField())).filter(json__row_id=int(row_id))
        return queryset
