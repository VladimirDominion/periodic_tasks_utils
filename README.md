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

celery --app=<your_app> beat --scheduler periodic_tasks_api.schedulers.CustomDatabaseScheduler
```

```
## API call examples:
GET /periodic_task/?task_type__in=auto-sync&task_type__in=email&jkwargs__row_id=821

POST /periodic_task/
```json
{
    "kwargs": {"row_id": 821},
    "enabled": true,
    "description": "",
    "task_type": "auto-sync",
    "cron_tab_data": {
        "minute": 0,
        "hour": 7,
        "timezone": "UTC"
    }
}
```

```json
{
    "kwargs": {"row_id": 821},
    "enabled": false,
    "description": "",
    "task_type": "auto-sync"
}
```

PUT /periodic_task/<id>/
<body>
```json
{
    "kwargs": {"row_id": 821},
    "enabled": true,
    "description": "",
    "task_type": "auto-sync"
}
```

DELETE /periodic_task/<id>/

```python
PERIODIC_TASK_API_CONFIG = [
    {
        "task_type": "auto-sync",  # required
        "path_to_task": "audience.tasks.run_pii_audiences_update",  # required
        "kwargs_serializer": 'rest_framework.serializers.Serializer',  # optional but recommended
        "label": "Auto sync task",  # optional,
        "command_model": "campaign.models.FacebookCampaign",
        "command_field_key": "social_campaign_id",
        "cron_tab_data": {
            "minute": 0,
            "hour": 6,
            "timezone": "UTC",
        },  # Temporary required
    }
]

```

```python
python manage.py get_or_create_periodic_tasks

# VERY IMPORTANT - UI should save values to kwargs as STRINGS, otherwise filtering will not work.

## Methods

- GET - return list of tasks (Filter by jkwargs__<field_in_kwargs>, and filtering by other model fields);
- POST - create periodic task(cron tab support only);
- PUT - update periodic task fields
- DELETE  - remove periodic task;
- OPTIONS - return structure of object and field choices;
