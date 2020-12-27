from django.contrib import admin


from .view_set_models import ViewSet
from .attr_models import Attr
from .anomaly_models import Anomaly
from .sample_set_models import SampleSet
from .sample_set_upload_models import SampleSetUpload
from .task_models import Task


@admin.register(ViewSet, Attr, Anomaly, SampleSet, SampleSetUpload, Task)
class AllModel(admin.ModelAdmin):
    pass


