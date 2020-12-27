from django_filters.rest_framework import FilterSet
from django_filters import filters
from MetisModels.sample_set_models import SampleSet
from MetisModels.sample_set_upload_models import SampleSetUpload


class SampleFilter(FilterSet):
    train_or_test = filters.CharFilter(field_name='train_or_test', lookup_expr='icontains')
    source = filters.CharFilter(field_name='source', lookup_expr='icontains')

    class Meta:
        model = SampleSet
        fields = ['train_or_test',  'source']


class SampleUploadFilter(FilterSet):
    file_name = filters.CharFilter(field_name='file_name', lookup_expr='icontains')

    class Meta:
        model = SampleSetUpload
        fields = ['file_name']