from MetisModels.view_set_models import ViewSet
from .serializers import ViewSetListSerializer, ViewSetUpdateSetSerializer, ViewSetCreateSetSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.error_code import *
from utils.utils import build_ret_data, render_json
from utils.pagination import PNPagination
from .filters import ViewSetFilter


class ViewSetListView(ListAPIView):
    queryset = ViewSet.objects.all()
    serializer_class = ViewSetListSerializer
    pagination_class = PNPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = ViewSetFilter
    ordering_fields = ['id']

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class ViewSetCreateView(CreateAPIView):
    serializer_class = ViewSetCreateSetSerializer

    def post(self, request):
        req_data = request.data
        data = dict()

        data['view_set_id'] = req_data['viewSetId']
        data['view_set_name'] = req_data['viewSetName']
        data['description'] = req_data['description']
        # 从drf的request中获取用户(对django的request作了扩展的)
        data['create_user'] = request.user.id
        serializer = ViewSetCreateSetSerializer(data=data)
        if serializer.is_valid() is False:
            return_dict = build_ret_data(THROW_EXP, str(serializer.errors))
            return render_json(return_dict)
        data = serializer.validated_data
        ViewSet.objects.create(**data)
        return_dict = build_ret_data(OP_SUCCESS, serializer.data)
        return render_json(return_dict)


class ViewSetUpdateView(UpdateAPIView):
    """
        url获取pk,修改时指定序列化类和query_set
    """
    model = ViewSet
    serializer_class = ViewSetUpdateSetSerializer
    queryset = model.objects.all()

    # 前端使用patch方法，到达这里
    def patch(self, request, *args, **kwargs):
        req_data = request.data
        vid = req_data['id']
        view_set_id = req_data['viewSetId']
        view_set_name = req_data['viewSetName']
        description = req_data['description']
        # 这样更新，可以把那些update_date字段自动更新，而使用filter().update()则是不会
        try:
            _v = ViewSet.objects.get(id=vid)
            _v.view_set_id = view_set_id
            _v.view_set_name = view_set_name
            _v.description = description
            _v.save()
            return_dict = build_ret_data(OP_SUCCESS, str(req_data))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


class ViewSetDestroyView(DestroyAPIView):
    queryset = ViewSet.objects.all()

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