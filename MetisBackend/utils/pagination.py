from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import FilterSet
from django_filters import filters
from MetisModels.models import TrainTask
from MetisModels.models import SampleSet


class PNPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'pageSize'
    page_query_param = 'currentPage'

    '''
    age_query_param：表示url中的页码参数
    page_size_query_param：表示url中每页数量参数
    page_size：表示每页的默认显示数量
    max_page_size：表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃
    '''


class LOPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    limit_query_param = 'pageSize'
    offset_query_param = 'currentPage'

    '''
    default_limit：表示默认每页显示几条数据
    limit_query_param：表示url中本页需要显示数量参数
    offset_query_param：表示从数据库中的第几条数据开始显示参数
    max_limit：表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃
    '''


class TaskFilter(FilterSet):
    task_id = filters.CharFilter(field_name='task_id', lookup_expr='icontains')
    model_name = filters.CharFilter(field_name='model_name', lookup_expr='icontains')
    source = filters.AllValuesMultipleFilter(field_name='source', lookup_expr='icontains')

    class Meta:
        model = TrainTask
        fields = ['task_id', 'model_name', 'source']


class SampleFilter(FilterSet):
    train_or_test = filters.CharFilter(field_name='train_or_test', lookup_expr='icontains')
    source = filters.CharFilter(field_name='source', lookup_expr='icontains')

    class Meta:
        model = SampleSet
        fields = ['train_or_test',  'source']