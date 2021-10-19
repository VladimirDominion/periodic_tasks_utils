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
    'periodic_tasks_api'
]

AUTO_SYNC_TASK_PATH = 'proj.tasks.task_name'
```
## Usage

```python

``auto-sync/`` url:


```python
urlpatterns = [
    url(
        r'^api/your_service/V1/',
        include("periodic_tasks_api.urls"),
    ),
]
```

celery --app=<your_app> beat --scheduler periodic_tasks_api.schedulers.CustomDatabaseScheduler

## Methods

- GET - return list of tasks (Filter by row_id: use with ``row_id=value`` query params);
- POST - create periodic task(cron tab support only);
- PUT - update periodic task fields
- DELETE  - remove periodic task;
- OPTIONS - return structure of object and field choices;
