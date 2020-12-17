from MetisModels.models import ViewSet
from MetisModels.models import Attr
from .serializers import ViewSetSerializer
from .serializers import AttrSerializer
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.error_code import *
from utils.utils import build_ret_data, render_json
from utils.pagination import PNPagination
from utils.filters import ViewSetFilter
from utils.filters import AttrFilter


class ViewSetListView(ListAPIView):
    queryset = ViewSet.objects.all()
    serializer_class = ViewSetSerializer
    pagination_class = PNPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = ViewSetFilter
    ordering_fields = ['id']

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class AttrListView(ListAPIView):
    pagination_class = PNPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = AttrFilter
    ordering_fields = ['id']

    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        print(query_params)
        view_set_id = query_params.get('viewSetId')
        attr_sets = Attr.objects.filter(view_set__id=view_set_id)
        # 创建分页对象
        pg = PNPagination()
        # 在数据库中获取分页数据
        pager_tasks = pg.paginate_queryset(queryset=attr_sets, request=request, view=self)
        # 对分页数据进行序列化
        serializer = AttrSerializer(instance=pager_tasks, many=True)
        # 不带分页时，直接输出
        # serializer = TrainTaskSerializer(instance=task_sets, many=True)
        # print(serializer.data)
        return_dict = build_ret_data(OP_SUCCESS, serializer.data)
        return render_json(return_dict)
