import importlib

from django.conf import settings
from django.core.exceptions import ValidationError


def get_entity_from_path_string(entity_path):
    mod_name, entity_name = entity_path.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, entity_name)
    return func


def get_periodic_tasks_config() -> list:
    conf = getattr(settings, "PERIODIC_TASK_API_CONFIG", None)
    if not conf:
        raise ValidationError("You have no configured PERIODIC_TASK_API_CONFIG.")
    return conf


def get_config_by_task_type(task_type):
    for task_config in get_periodic_tasks_config():
        if task_config["task_type"] == task_type:
            return task_config


def get_task_type_choices_from_config(context):
    choices = []
    for task_config in get_periodic_tasks_config():
        choices.append((
            task_config.get("task_type"),
            task_config.get("label") or task_config.get("task_type").replace('-', ' ').lower().capitalize()
        ))
    return choices
