from MetisModels.attr_models import Attr
from MetisModels.task_models import Task
from MetisModels.view_set_models import ViewSet
from .serializers import AttrListSerializer, AttrCreateSerializer, AttrUpdateSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.error_code import *
from utils.utils import build_ret_data, render_json
from utils.pagination import PNPagination
from .filters import AttrFilter


class AttrListView(ListAPIView):
    queryset = Attr.objects.all()
    serializer_class = AttrListSerializer
    pagination_class = PNPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = AttrFilter
    ordering_fields = ['id']

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class AttrCreateView(CreateAPIView):
    serializer_class = AttrCreateSerializer

    def post(self, request):
        req_data = request.data
        print(req_data)
        data = dict()
        data['attr_id'] = req_data['attrId']
        data['attr_name'] = req_data['attrName']
        data['description'] = req_data['description']
        data['view_set'] = req_data['viewSetId']
        data['model'] = req_data['modelId']
        data['security_token'] = req_data['securityToken']
        data['check_security'] = req_data['checkSecurity']
        data['url'] = req_data['url']
        # 从drf的request中获取用户(对django的request作了扩展的)
        data['create_user'] = request.user.id
        serializer = AttrCreateSerializer(data=data)
        if serializer.is_valid() is False:
            return_dict = build_ret_data(THROW_EXP, str(serializer.errors))
            return render_json(return_dict)
        data = serializer.validated_data
        try:
            Attr.objects.create(**data)
            return_dict = build_ret_data(OP_SUCCESS, serializer.data)
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


class AttrUpdateView(UpdateAPIView):
    """
        url获取pk,修改时指定序列化类和query_set
    """
    model = Attr
    serializer_class = AttrUpdateSerializer
    queryset = model.objects.all()

    # 前端使用patch方法，到达这里
    def patch(self, request, *args, **kwargs):
        req_data = request.data
        print(req_data, "####")
        aid = req_data['id']
        attr_id = req_data['attrId']
        attr_name = req_data['attrName']
        description = req_data['description']
        view_set_id = req_data['viewSetId']
        view_set = ViewSet.objects.get(id=view_set_id)
        model_id = req_data['modelId']
        model = Task.objects.get(id=model_id)
        security_token = req_data['securityToken']
        check_security = req_data['checkSecurity']
        url = req_data['url']
        # 这样更新，可以把那些update_date字段自动更新，而使用filter().update()则是不会
        try:
            _a = Attr.objects.get(id=aid)
            _a.attr_id = attr_id
            _a.attr_name = attr_name
            _a.description = description
            _a.model = model
            _a.view_set = view_set
            _a.security_token = security_token
            _a.check_security = check_security
            _a.url = url
            _a.save()
            return_dict = build_ret_data(OP_SUCCESS, str(req_data))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


class AttrDestroyView(DestroyAPIView):
    queryset = Attr.objects.all()

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