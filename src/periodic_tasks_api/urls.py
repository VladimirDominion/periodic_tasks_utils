from django.urls import path

from periodic_tasks_api.views import AutoSyncView

urlpatterns = [
    path('auto-sync/', AutoSyncView.as_view())
]
