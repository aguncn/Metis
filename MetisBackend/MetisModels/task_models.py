from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# 训练任务
class Task(models.Model):
    task_id = models.CharField(max_length=255,
                               unique=True,
                               verbose_name='训练任务ID')
    sample_num = models.IntegerField(verbose_name='样本总量')
    positive_sample_num = models.IntegerField(verbose_name='正样本数量')
    negative_sample_num = models.IntegerField(verbose_name='负样本数量')
    window = models.IntegerField(verbose_name='时间窗口')
    model_name = models.CharField(max_length=64,
                                  verbose_name='模型名称')
    source = models.CharField(max_length=32,
                              default='metis',
                              verbose_name='来源')
    start_date = models.DateTimeField(verbose_name='开始训练时间')
    end_date = models.DateTimeField(verbose_name='结束训练时间')
    create_user = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='ra_train_task',
                                    on_delete=models.DO_NOTHING,
                                    verbose_name='创建者')
    task_status = models.CharField(max_length=16,
                                   null=True,
                                   blank=True,
                                   verbose_name='任务状态')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='新建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.BooleanField(default=True, verbose_name='状态')

    @property
    def username(self):
        return self.create_user.username

    def __str__(self):
        return self.model_name

    class Meta:
        db_table = 'Task'
        ordering = ('-update_date', )