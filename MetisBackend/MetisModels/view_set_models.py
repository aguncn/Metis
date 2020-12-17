from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# 指标集
class ViewSet(models.Model):
    view_set_id = models.CharField(max_length=64,
                                   unique=True,
                                   verbose_name='指标集id')
    view_set_name = models.CharField(max_length=64,
                                     unique=True,
                                     verbose_name='指标集名称')
    description = models.CharField(max_length=1024,
                                   null=True,
                                   blank=True,
                                   verbose_name='指标集描述')
    create_user = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='ra_view_set',
                                    on_delete=models.DO_NOTHING,
                                    verbose_name='创建者')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='新建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.BooleanField(default=True, verbose_name='状态')

    @property
    def username(self):
        return self.create_user.username

    @property
    def attr_count(self):
        return self.ra_attr.count()

    def __str__(self):
        return self.view_set_name

    class Meta:
        db_table = 'ViewSet'
        ordering = ('-update_date', )