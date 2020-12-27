from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


# 让上传的文件路径动态地与user的名字有关
def upload_to(instance, filename):
    return '/'.join([settings.MEDIA_ROOT, instance.create_user.username, filename])


# 样本库
class SampleSetUpload(models.Model):
    sample_set_upload_id = models.CharField(max_length=255,
                                            unique=True,
                                            verbose_name='上传任务ID')
    sample_count = models.IntegerField(default=0,
                                       verbose_name='样本数量')
    file_name = models.CharField(max_length=255,
                                 verbose_name='上传文件名')
    file_path = models.FileField(upload_to=upload_to)
    create_user = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='ra_sample_set_upload',
                                    on_delete=models.DO_NOTHING,
                                    verbose_name='上传者')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='新建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.BooleanField(default=True, verbose_name='状态')

    @property
    def username(self):
        return self.create_user.username

    def __str__(self):
        return self.sample_set_upload_id

    class Meta:
        db_table = 'SampleSetUpload'
        ordering = ('-update_date', )
