from django.db import models
from django.contrib.auth import get_user_model
from .attr_models import Attr

User = get_user_model()


# 异常库
class Anomaly(models.Model):
    attr = models.ForeignKey(Attr,
                             related_name='ra_anomaly',
                             null=True,
                             blank=True,
                             on_delete=models.DO_NOTHING,
                             verbose_name='指标')
    anomaly_time = models.DateTimeField(verbose_name='异常检测时间')
    data_a = models.TextField(verbose_name='当天180分钟数据')
    data_b = models.TextField(verbose_name='一天前180分钟数据')
    data_c = models.TextField(verbose_name='一周前180分钟数据')
    check_anomaly = models.BooleanField(default=True,
                                        verbose_name='是否异常')
    mark_flag = models.CharField(max_length=16,
                                 null=True,
                                 blank=True,
                                 verbose_name='标注正负样本')
    create_user = models.ForeignKey(User,
                                    related_name='ra_anomaly',
                                    null=True,
                                    blank=True,
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
        db_table = 'Anomaly'
        ordering = ('-update_date', )

