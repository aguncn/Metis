from django_filters.rest_framework import FilterSet
from django_filters import filters
from MetisModels.models import ViewSet
from MetisModels.models import Attr


class ViewSetFilter(FilterSet):
    view_name = filters.CharFilter(field_name='view_name', lookup_expr='icontains')

    class Meta:
        model = ViewSet
        fields = ['view_name']


class AttrFilter(FilterSet):
    attr_name = filters.CharFilter(field_name='attr_name', lookup_expr='icontains')

    class Meta:
        model = Attr
        fields = ['attr_name']
