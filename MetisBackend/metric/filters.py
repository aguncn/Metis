from django_filters.rest_framework import FilterSet
from django_filters import filters
from MetisModels.view_set_models import ViewSet
from MetisModels.attr_models import Attr


class ViewSetFilter(FilterSet):
    view_set_id = filters.CharFilter(field_name='view_set_id', lookup_expr='icontains')
    view_set_name = filters.CharFilter(field_name='view_set_name', lookup_expr='icontains')

    class Meta:
        model = ViewSet
        fields = ['view_set_id', 'view_set_name']


class AttrFilter(FilterSet):
    attr_id = filters.CharFilter(field_name='attr_id', lookup_expr='icontains')
    attr_name = filters.CharFilter(field_name='attr_name', lookup_expr='icontains')

    class Meta:
        model = Attr
        fields = ['attr_id', 'attr_name']