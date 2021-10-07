from django.urls import path

from .views import AutoSyncView

urlpatterns = [
    path('auto-sync/', AutoSyncView.as_view())
]
