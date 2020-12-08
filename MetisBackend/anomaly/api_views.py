from MetisModels.models import Anomaly
from .serializers import AnomalySerializer
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.error_code import *
from utils.utils import build_ret_data, render_json
from utils.pagination import PNPagination, AnomalyFilter


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