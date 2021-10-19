from rest_framework.routers import DefaultRouter

from periodic_tasks_api.views import PeriodicTaskView


router = DefaultRouter()
router.register(
    r'periodic_task',
    PeriodicTaskView,
    basename='periodic-tasks'
)

urlpatterns = [] + router.urls
