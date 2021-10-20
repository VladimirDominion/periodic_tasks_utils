from rest_framework import viewsets

from periodic_tasks_api.models import CustomExtendedPeriodicTask
from periodic_tasks_api.serializers import PeriodicTaskSerializer
from periodic_tasks_api.filters import PeriodicTaskFilterSet


class PeriodicTaskView(viewsets.ModelViewSet):
    queryset = CustomExtendedPeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
    filter_backends = [PeriodicTaskFilterSet]
