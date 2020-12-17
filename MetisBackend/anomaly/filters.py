from django.db.models import Q
from django_filters.rest_framework import FilterSet
from django_filters import filters
from MetisModels.anomaly_models import Anomaly


class AnomalyFilter(FilterSet):
    attr = filters.CharFilter(field_name='attr__attr_name', lookup_expr='icontains',)
    view_set = filters.CharFilter(field_name='attr__view_set__view_name', lookup_expr='icontains',)
    begin_time = filters.CharFilter(field_name='anomaly_time', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='anomaly_time', lookup_expr='lte',)
    mark_flag = filters.CharFilter(field_name='mark_flag', method='mark_flag_filter',)

    def mark_flag_filter(self, queryset, field_name, value):
        print(value)
        if value == 'no':
            return queryset.filter(~Q(mark_flag='negative') & ~Q(mark_flag='positive'))
        elif value == 'yes':
            return queryset.filter(Q(mark_flag='negative') | Q(mark_flag='positive'))
        elif value == 'all':
            return queryset
        else:
            return queryset

    class Meta:
        model = Anomaly
        fields = ['attr', 'view_set', 'begin_time', 'end_time', 'anomaly_time', 'mark_flag']
