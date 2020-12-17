from MetisModels.anomaly_models import Anomaly
from MetisModels.sample_set_models import SampleSet
from .serializers import AnomalySerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.error_code import *
from utils.utils import build_ret_data, render_json
from utils.pagination import PNPagination
from .filters import AnomalyFilter


class AnomalyListView(ListAPIView):
    queryset = Anomaly.objects.all()
    serializer_class = AnomalySerializer
    pagination_class = PNPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = AnomalyFilter
    ordering_fields = ['id']

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class AnomalyUpdateView(APIView):
    def post(self, request):
        req_data = request.data
        aid = req_data['anomalyId']
        mark_flag = req_data['markFlag']
        if mark_flag == 'positive' or mark_flag == 'negative':
            try:
                _a = Anomaly.objects.get(id=aid)
                _a.mark_flag = mark_flag
                _a.save()
                attr = _a.attr
                data_a = _a.data_a
                data_b = _a.data_b
                data_c = _a.data_c
                anomaly_time = _a.anomaly_time
                source = "unknown"
                train_or_test = "train"
                positive_or_negative = mark_flag
                window = data_a.count(',')
                anomaly = _a
                create_user = request.user

                SampleSet.objects.create(
                    attr=attr,
                    source=source,
                    train_or_test=train_or_test,
                    positive_or_negative=positive_or_negative,
                    window=window,
                    anomaly_time=anomaly_time,
                    data_a=data_a,
                    data_b=data_b,
                    data_c=data_c,
                    anomaly=anomaly,
                    create_user=create_user
                )
                return_dict = build_ret_data(OP_SUCCESS, str(req_data))
                return render_json(return_dict)
            except Exception as e:
                print(e)
                return_dict = build_ret_data(THROW_EXP, str(e))
                return render_json(return_dict)
        else:
            _a = Anomaly.objects.get(id=aid)
            _a.mark_flag = ''
            _a.save()
            SampleSet.objects.filter(anomaly=_a).delete()
            return_dict = build_ret_data(OP_SUCCESS, str(req_data))
            return render_json(return_dict)
