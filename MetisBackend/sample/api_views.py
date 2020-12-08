from MetisModels.models import SampleSet
from rest_framework.views import APIView
from django.utils import timezone
from .serializers import SampleSetSerializer
from .serializers import SampleUpdateSetSerializer
from rest_framework.generics import ListAPIView
from rest_framework.generics import UpdateAPIView
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


class SampleUpdateView(UpdateAPIView):
    """
        url获取pk,修改时指定序列化类和query_set
        """
    model = SampleSet
    serializer_class = SampleUpdateSetSerializer
    queryset = model.objects.all()

    # 前端使用patch方法，到达这里
    def patch(self, request, *args, **kwargs):
        req_data = request.data
        sid = req_data['id']
        source = req_data['source']
        train_or_test = req_data['trainTest']
        positive_or_negative = req_data['positiveNegative']
        # 这样更新，可以把那些update_date字段自动更新，而使用filter().update()则是不会
        try:
            _t = SampleSet.objects.get(id=sid)
            _t.source = source
            _t.train_or_test = train_or_test
            _t.positive_or_negative = positive_or_negative
            _t.save()
            return_dict = build_ret_data(OP_SUCCESS, str(req_data))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


class SampleDestroyView(DestroyAPIView):
    queryset = SampleSet.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            res = super().destroy(self, request, *args, **kwargs)
            return_dict = build_ret_data(OP_SUCCESS, str(res))
            print(res)
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)