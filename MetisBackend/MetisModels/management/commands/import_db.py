from datetime import datetime
from django.utils import timezone
import pytz
import random
from django.core.management.base import BaseCommand, CommandError
from .utils import get_anomaly, get_sample_set
from MetisModels.view_set_models import ViewSet
from MetisModels.attr_models import Attr
from MetisModels.anomaly_models import Anomaly
from MetisModels.sample_set_models import SampleSet
from MetisModels.task_models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

user_name = 'admin'


class Command(BaseCommand):
    help = '将模拟数据导入数据库'

    def add_arguments(self, parser):
        parser.add_argument('db_name', type=str, help='导入所有数据')

    def handle(self, *args, **options):
        db_name = options['db_name']
        self.add_user()
        self.add_view_set()
        self.add_attr()
        self.add_anomaly()
        self.add_sample_set()
        self.add_train_task()
        self.stdout.write('模拟数据导入完成')

    # 新建一个用户
    def add_user(self):
        try:
            result = User.objects.get(username=user_name)
            result.delete()
        except User.DoesNotExist as e:
            print(e)
        User.objects.create_user(username=user_name,
                                 password='password',
                                 is_staff=True,
                                 is_active=True,
                                 is_superuser=True)
        self.stdout.write('用户{}重建完成。'.format(user_name))

    # 新建一个多个指标集
    def add_view_set(self):
        ViewSet.objects.all().delete()
        user = User.objects.get(username=user_name)
        ViewSet.objects.create(view_set_id='1001', view_set_name='系统性能', description='系统性能', create_user=user)
        ViewSet.objects.create(view_set_id='1002', view_set_name='网络流量', description='网络流量', create_user=user)
        ViewSet.objects.create(view_set_id='1003', view_set_name='用户登陆', description='用户登陆', create_user=user)
        ViewSet.objects.create(view_set_id='1004', view_set_name='中间件连接', description='中间件连接', create_user=user)
        ViewSet.objects.create(view_set_id='1005', view_set_name='数据库性能', description='数据库性能', create_user=user)
        self.stdout.write('ViewSet数据表删除并重建完成。')

    # 新建多个指标
    def add_attr(self):
        Attr.objects.all().delete()
        view_set = ViewSet.objects.get(view_set_name='系统性能')
        Attr.objects.create(attr_id='50001', attr_name='CPU负载', view_set=view_set)
        Attr.objects.create(attr_id='50002', attr_name='内存负载', view_set=view_set)
        view_set = ViewSet.objects.get(view_set_name='网络流量')
        Attr.objects.create(attr_id='50003', attr_name='上海机房', view_set=view_set)
        Attr.objects.create(attr_id='50004', attr_name='北京机房', view_set=view_set)
        view_set = ViewSet.objects.get(view_set_name='用户登陆')
        Attr.objects.create(attr_id='50005', attr_name='登陆时长', view_set=view_set)
        view_set = ViewSet.objects.get(view_set_name='中间件连接')
        Attr.objects.create(attr_id='50007', attr_name='Redis连接数', view_set=view_set)
        Attr.objects.create(attr_id='50008', attr_name='Kafka吞吐量', view_set=view_set)
        self.stdout.write('Attr数据表删除并重建完成。')

    # 增加模拟的异常数据
    def add_anomaly(self):
        Anomaly.objects.all().delete()
        data_a, data_b, data_c = get_anomaly()
        user = User.objects.get(username=user_name)
        for (a, b, c) in zip(data_a, data_b, data_c):
            anomaly_time = timezone.now() + timezone.timedelta(hours=random.randint(1, 10))
            attr = Attr.objects.order_by('?').first()
            Anomaly.objects.create(
                attr=attr,
                anomaly_time=anomaly_time,
                data_a=a,
                data_b=b,
                data_c=c,
                create_user=user,
            )

        self.stdout.write('Anomaly数据表删除并重建完成。')

    # 增加模拟的样本库
    def add_sample_set(self):
        SampleSet.objects.all().delete()

        data_a, data_b, data_c = get_sample_set()
        user = User.objects.get(username=user_name)
        for (a, b, c) in zip(data_a, data_b, data_c):
            anomaly_time = timezone.now() + timezone.timedelta(hours=random.randint(1, 10))
            attr = Attr.objects.order_by('?').first()
            SampleSet.objects.create(
                attr=attr,
                train_or_test=random.choice(['train', 'test']),
                positive_or_negative=random.choice(['positive', 'negative']),
                window=180,
                anomaly_time=anomaly_time,
                data_a=a,
                data_b=b,
                data_c=c,
                create_user=user,
            )

        self.stdout.write('SampleSet数据表删除并重建完成。')

    # 增加两个训练任务，没有关联哟，只为有数据记录
    def add_train_task(self):
        Task.objects.all().delete()
        user = User.objects.get(username=user_name)
        Task.objects.create(
            task_id='1535790960079',
            sample_num=90675,
            positive_sample_num=45228,
            negative_sample_num=45447,
            window=180,
            model_name='xgb_default_model',
            source='metis',
            start_date=timezone.now() - timezone.timedelta(hours=random.randint(1, 10)),
            end_date=timezone.now(),
            create_user=user,
            task_status='running',
        )
        Task.objects.create(
            task_id='1535790964836',
            sample_num=88675,
            positive_sample_num=44228,
            negative_sample_num=44447,
            window=180,
            model_name='xgb_2nd_model',
            source='metis',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(hours=random.randint(1, 10)),
            create_user=user,
            task_status='finish',
        )
        self.stdout.write('TrainTask数据表删除并重建完成。')


def str_to_datetime(time_str):
    return datetime.strptime(time_str,
                             '%Y-%m-%d %H:%M:%S')\
        .replace(tzinfo=(pytz.timezone('Asia/Shanghai')))
