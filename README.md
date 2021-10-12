# periodic_tasks_utils

periodic_tasks_utils is a Python library that allow to control periodic tasks for django-celery-beat.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install git+https://bitbucket.org/myntelligence_v2/periodic_tasks_utils/
```

``
settings.py
``
```python

INSTALLED_APPS = [
    ...,
    'django_celery_beat',
]

AUTO_SYNC_TASK_PATH = 'proj.tasks.task_name'
```
## Usage

```python
from periodic_tasks_utils.views import AutoSyncView

urlpatterns = [
    path('route_name/', AutoSyncView.as_view())
]
```

or with default ``auto-sync/`` url:

```python
urlpatterns = [
    path('', include("periodic_tasks_api.urls")) 
]
```
