from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# 指标集
class ViewSet(models.Model):
    view_id = models.CharField(max_length=64,
                               verbose_name='指标集id')
    view_name = models.CharField(max_length=64,
                                 verbose_name='指标集名称')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='新建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __str__(self):
        return self.view_name

    @property
    def username(self):
        return self.create_user.username

    @property
    def attr_count(self):
        return self.ra_attr.count()

    class Meta:
        db_table = 'ViewSet'
        ordering = ('-update_date', )


# 指标
class Attr(models.Model):
    attr_id = models.CharField(max_length=64,
                               verbose_name='指标id')
    attr_name = models.CharField(max_length=64,
                                 verbose_name='指标名称')
    view_set = models.ForeignKey(ViewSet,
                                 related_name='ra_attr',
                                 on_delete=models.CASCADE,
                                 verbose_name='指标集')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='新建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.BooleanField(default=True, verbose_name='状态')

    @property
    def username(self):
        return self.create_user.username

    @property
    def view_set_name(self):
        return self.attr.view_set.view_name

    def __str__(self):
        return self.attr_name

    class Meta:
        db_table = 'Attr'
        ordering = ('-update_date',)


# 异常库
class Anomaly(models.Model):
    attr = models.ForeignKey(Attr,
                             related_name='ra_anomaly',
                             on_delete=models.CASCADE,
                             verbose_name='指标')
    anomaly_time = models.DateTimeField(verbose_name='异常检测时间')
    data_a = models.TextField(verbose_name='当天180分钟数据')
    data_b = models.TextField(verbose_name='一天前180分钟数据')
    data_c = models.TextField(verbose_name='一周前180分钟数据')
    mark_flag = models.CharField(max_length=16,
                                 null=True,
                                 blank=True,
                                 verbose_name='标注正负样本')
    create_user = models.ForeignKey(User,
                                    related_name='ra_anomaly',
                                    on_delete=models.CASCADE,
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
        return self.attr.view_set.view_name

    def __str__(self):
        return self.attr.attr_name

    class Meta:
        db_table = 'Anomaly'
        ordering = ('-update_date', )


# 样本库
class SampleSet(models.Model):
    attr = models.ForeignKey(Attr,
                             related_name='ra_sample_set',
                             on_delete=models.CASCADE,
                             verbose_name='指标')
    source = models.CharField(max_length=32,
                              default='Metis',
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
                                on_delete=models.CASCADE,
                                verbose_name='关联异常')
    create_user = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='ra_sample_set',
                                    on_delete=models.CASCADE,
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
        return self.attr.view_set.view_name

    def __str__(self):
        return self.attr.attr_name

    class Meta:
        db_table = 'SampleSet'
        ordering = ('-update_date', )


# 训练任务
class TrainTask(models.Model):
    task_id = models.CharField(max_length=255,
                               verbose_name='训练任务ID')
    sample_num = models.IntegerField(verbose_name='样本总量')
    positive_sample_num = models.IntegerField(verbose_name='正样本数量')
    negative_sample_num = models.IntegerField(verbose_name='负样本数量')
    window = models.IntegerField(verbose_name='时间窗口')
    model_name = models.CharField(max_length=64,
                                  verbose_name='模型名称')
    source = models.CharField(max_length=32,
                              default='Metis',
                              verbose_name='来源')
    start_date = models.DateTimeField(verbose_name='开始训练时间')
    end_date = models.DateTimeField(verbose_name='结束训练时间')
    create_user = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='ra_train_task',
                                    on_delete=models.CASCADE,
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
        db_table = 'TrainTask'
        ordering = ('-update_date', )


