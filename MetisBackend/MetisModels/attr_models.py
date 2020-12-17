from django.db import models
from django.contrib.auth import get_user_model
from .view_set_models import ViewSet
from .task_models import Task

User = get_user_model()


# 指标
class Attr(models.Model):
    attr_id = models.CharField(max_length=64,
                               unique=True,
                               verbose_name='指标id')
    attr_name = models.CharField(max_length=64,
                                 unique=True,
                                 verbose_name='指标名称')
    view_set = models.ForeignKey(ViewSet,
                                 null=True,
                                 blank=True,
                                 related_name='ra_attr',
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='指标集')
    description = models.CharField(max_length=1024,
                                   null=True,
                                   blank=True,
                                   verbose_name='指标描述')
    model = models.ForeignKey(Task,
                              null=True,
                              blank=True,
                              related_name='ra_attr',
                              on_delete=models.DO_NOTHING,
                              verbose_name='关联模型')
    security_token = models.CharField(max_length=64,
                                      null=True,
                                      blank=True,
                                      verbose_name='连接token')
    check_security = models.BooleanField(default=False,
                                         verbose_name='启用token保护')
    url = models.CharField(max_length=1024,
                           null=True,
                           blank=True,
                           verbose_name='监控url')
    create_user = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='ra_attr',
                                    on_delete=models.DO_NOTHING,
                                    verbose_name='创建者')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='新建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.BooleanField(default=True, verbose_name='状态')

    @property
    def username(self):
        return self.create_user.username

    @property
    def view_set_name(self):
        return self.view_set.view_set_name

    # 特别注意，此处的model_name的名称，不能和字段定义中的model名称相同。如果相同，则同名字段不能合进数据库。
    @property
    def model_name(self):
        return self.model.model_name

    def __str__(self):
        return self.attr_name

    class Meta:
        db_table = 'Attr'
        ordering = ('-update_date',)
