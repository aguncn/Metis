from django.db import models
from django.contrib.auth import get_user_model
from .attr_models import Attr
from .anomaly_models import Anomaly

User = get_user_model()


# 样本库
class SampleSet(models.Model):
    attr = models.ForeignKey(Attr,
                             related_name='ra_sample_set',
                             null=True,
                             blank=True,
                             on_delete=models.DO_NOTHING,
                             verbose_name='指标')
    source = models.CharField(max_length=32,
                              default='metis',
                              verbose_name='来源')
    train_or_test = models.CharField(max_length=32,
                                     null=True,
                                     blank=True,
                                     verbose_name='训练集OR测试集')
    positive_or_negative = models.CharField(max_length=32,
                                            null=True,
                                            blank=True,
                                            verbose_name='正样本OR负样本')
    window = models.IntegerField(verbose_name='时间窗口')
    anomaly_time = models.DateTimeField(verbose_name='异常检测时间')
    data_a = models.TextField(verbose_name='当天180分钟数据')
    data_b = models.TextField(verbose_name='一天前360分钟数据')
    data_c = models.TextField(verbose_name='一周前360分钟数据')
    anomaly = models.ForeignKey(Anomaly,
                                null=True,
                                blank=True,
                                related_name='ra_sample_set',
                                on_delete=models.DO_NOTHING,
                                verbose_name='关联异常')
    create_user = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='ra_sample_set',
                                    on_delete=models.DO_NOTHING,
                                    verbose_name='创建者')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='新建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.BooleanField(default=True, verbose_name='状态')

    @property
    def username(self):
        return self.create_user.username

    @property
    def attr_name(self):
        return self.attr.attr_name

    @property
    def view_set_name(self):
        return self.attr.view_set.view_set_name

    def __str__(self):
        return self.attr.attr_name

    class Meta:
        db_table = 'SampleSet'
        ordering = ('-update_date', )

