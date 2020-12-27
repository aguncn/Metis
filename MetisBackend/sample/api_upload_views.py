import time
import traceback
import csv
from django.contrib.auth import get_user_model
from MetisModels.sample_set_models import SampleSet
from MetisModels.attr_models import Attr
from MetisModels.sample_set_upload_models import SampleSetUpload
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.error_code import *
from utils.utils import build_ret_data, render_json
from utils.pagination import PNPagination
from .serializers import SampleUploadSerializer
from .filters import SampleUploadFilter

User = get_user_model()


class UploadSampleListView(ListAPIView):
    queryset = SampleSetUpload.objects.all()
    serializer_class = SampleUploadSerializer
    pagination_class = PNPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = SampleUploadFilter
    ordering_fields = ['id']

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class UploadSampleDestroyView(DestroyAPIView):
    queryset = SampleSetUpload.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            res = super().destroy(self, request, *args, **kwargs)
            return_dict = build_ret_data(OP_SUCCESS, str(res))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


# 上传样本文件
class UploadSampleView(APIView):

    def post(self, request, filename, format=None):
        try:
            # 前端的axios，最好不要用二次封装的，对请求头有统一处理，可能会传不过来。纯的axios可以搞定。
            file_path = request.data['file']
            uu_id = str(int(round(time.time() * 1000)))
            sample_set_upload_id = uu_id + '_sample_set'
            f = SampleSetUpload(sample_set_upload_id=sample_set_upload_id,
                                create_user=request.user,
                                file_name=filename,
                                file_path=file_path)
            f.save()
            csv_reader = csv.reader(open(str(f.file_path), encoding='utf-8'))
            next(csv_reader)
            for index, row in enumerate(csv_reader):
                create_user = request.user
                attr = Attr.objects.get(attr_name=row[2])
                source = row[5]
                train_or_test = row[6]
                positive_or_negative = row[7]
                anomaly_time = row[4]
                anomaly_time = '-'.join(anomaly_time.split('/'))
                data_a = row[8]
                window = len(data_a.split(',')) - 1
                data_b = row[9]
                data_c = row[10]
                upload = f
                SampleSet.objects.create(
                    attr=attr,
                    source=source,
                    train_or_test=train_or_test,
                    positive_or_negative=positive_or_negative,
                    anomaly_time=anomaly_time,
                    data_a=data_a,
                    data_b=data_b,
                    data_c=data_c,
                    window=window,
                    upload=upload,
                    create_user=create_user,
                )
            f.sample_count = index + 1
            f.save()
            return_dict = build_ret_data(OP_SUCCESS, str("res"))
            return render_json(return_dict)
        except Exception as e:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)
