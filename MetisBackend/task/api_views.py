import time
from django.utils import timezone
from MetisModels.task_models import Task
from .serializers import TaskSerializer
from .serializers import ModelSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.error_code import *
from utils.utils import build_ret_data, render_json
from utils.pagination import PNPagination
from .filters import TaskFilter


class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = PNPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['task_id', 'model_name']
    filter_class = TaskFilter
    # search_fields = ['task_id', 'model_name']
    ordering_fields = ['id']

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :return:

        query_params = request.query_params
        print(query_params)
        print(type(query_params))
        print(query_params.get('pageSize'))
        task_sets = TrainTask.objects.all()
        # 创建分页对象
        pg = PNPagination()
        # 在数据库中获取分页数据
        pager_tasks = pg.paginate_queryset(queryset=task_sets, request=request,view=self)
        # 对分页数据进行序列化
        serializer = TrainTaskSerializer(instance=pager_tasks, many=True)
        # 不带分页时，直接输出
        # serializer = TrainTaskSerializer(instance=task_sets, many=True)
        return_dict = build_ret_data(OP_SUCCESS, serializer.data)
        return render_json(return_dict)
        """
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class TaskCreateView(CreateAPIView):
    serializer_class = TaskSerializer

    def post(self, request):
        req_data = request.data
        data = dict()
        uu_id = str(int(round(time.time() * 1000)))
        data['task_id'] = uu_id
        data['model_name'] = uu_id + '_model'
        # 从drf的request中获取用户(对django的request作了扩展的)
        data['create_user'] = request.user.id
        data['negative_sample_num'] = req_data['negativeCount']
        data['positive_sample_num'] = req_data['positiveCount']
        data['sample_num'] = req_data['totalCount']
        data['source'] = ','.join(req_data['source'])
        data['window'] = 180
        start_date = timezone.datetime.strptime(req_data['beginTime'], '%Y-%m-%d')
        data['start_date'] = start_date
        end_date = timezone.datetime.strptime(req_data['endTime'], '%Y-%m-%d')
        data['end_date'] = end_date
        data['task_status'] = 'running'
        serializer = TaskSerializer(data=data)
        if serializer.is_valid() is False:
            return_dict = build_ret_data(THROW_EXP, str(serializer.errors))
            return render_json(return_dict)
        data = serializer.validated_data
        Task.objects.create(**data)
        return_dict = build_ret_data(OP_SUCCESS, serializer.data)
        return render_json(return_dict)


class TaskDestroyView(DestroyAPIView):
    queryset = Task.objects.all()
    """
    # 自定义get_object()方法，可以删除其它的其它数据，按return的项来删除
    def get_object(self, *args, **kwargs):
        user = self.request.user
        if user.username == 'admin':
            return user
        else:
            return None
    """

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


class ModelListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = ModelSerializer
    pagination_class = PNPagination

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)