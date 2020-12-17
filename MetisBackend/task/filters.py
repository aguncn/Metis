from django_filters.rest_framework import FilterSet
from django_filters import filters
from MetisModels.task_models import Task


class TaskFilter(FilterSet):
    task_id = filters.CharFilter(field_name='task_id', lookup_expr='icontains')
    model_name = filters.CharFilter(field_name='model_name', lookup_expr='icontains')
    source = filters.AllValuesMultipleFilter(field_name='source', lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['task_id', 'model_name', 'source']
