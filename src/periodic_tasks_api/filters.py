from django.core.exceptions import FieldError
from django.db.models import F
from django.db.models.functions import Cast
from django.contrib.postgres.fields import JSONField

from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import ValidationError


class PeriodicTaskFilterSet(BaseFilterBackend):

    kwargs_key = "jkwargs"

    def get_query_params(self, request):
        query_params = request.query_params.copy() or request.GET.copy()

        query_params_formated = {}
        for key in query_params.keys():
            if key.startswith(self.kwargs_key):
                query_params_formated[key] = query_params.get(key)
            else:
                query_params_formated[key] = query_params.getlist(key)

        return query_params_formated

    def _pop_kwargs(self, query_params):
        kwargs_params = {}
        for key, value in query_params.items():
            if key.startswith(self.kwargs_key):
                kwargs_params[key] = value

        for kwargs_key in kwargs_params.keys():
            if kwargs_key in query_params:
                query_params.pop(kwargs_key)

        return kwargs_params

    def filter_queryset(self, request, queryset, view):
        query_params = self.get_query_params(request)
        kwargs_params = self._pop_kwargs(query_params)

        try:
            queryset = queryset.filter(**query_params)
        except FieldError:
            raise ValidationError("Some of query parameters are wrong.")

        queryset = queryset.annotate(jkwargs=Cast(F('kwargs'), JSONField())).filter(**kwargs_params)

        return queryset
