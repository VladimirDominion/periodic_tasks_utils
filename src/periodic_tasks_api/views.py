from rest_framework import viewsets
from periodic_tasks_api.serializers import (
    PeriodicTaskInputSerializer,
)


class TaskView(viewsets.ModelViewSet):

    def get_serializer_class(self):
        serializers = {
            "get": PeriodicTaskInputSerializer
        }
        return
