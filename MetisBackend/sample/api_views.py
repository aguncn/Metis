from django.utils import timezone
from MetisModels.models import SampleSet
from .serializers import SampleSetSerializer
from rest_framework.views import APIView
from config.error_code import *
from utils.utils import build_ret_data, render_json
import time
from django.utils import timezone
from MetisModels.models import TrainTask
from .serializers import SampleSetSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.error_code import *
from utils.utils import build_ret_data, render_json
from utils.pagination import PNPagination, SampleFilter


class SampleSetCountView(APIView):
    def get(self, request):
        query_params = request.query_params
        begin_time = query_params.get('beginTime')
        begin_time = timezone.datetime.strptime(begin_time, '%Y-%m-%d')
        end_time = query_params.get('endTime')
        end_time = timezone.datetime.strptime(end_time, '%Y-%m-%d')
        source = query_params.getlist('source[]')
        source = [item.capitalize() for item in source]
        train_or_test = query_params.getlist('trainTest[]')
        positive_count = SampleSet.objects. \
            filter(update_date__range=[begin_time, end_time]). \
            filter(train_or_test__in=train_or_test). \
            filter(source__in=source). \
            filter(positive_or_negative='positive'). \
            count()
        negative_count = SampleSet.objects. \
            filter(update_date__range=[begin_time, end_time]). \
            filter(train_or_test__in=train_or_test). \
            filter(source__in=source). \
            filter(positive_or_negative='negative'). \
            count()
        data = {'negative_count': negative_count, 'positive_count': positive_count}
        return_dict = build_ret_data(OP_SUCCESS, data)
        return render_json(return_dict)


class SampleListView(ListAPIView):
    queryset = SampleSet.objects.all()
    serializer_class = SampleSetSerializer
    pagination_class = PNPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = SampleFilter
    ordering_fields = ['id']

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)