from django.contrib import admin


from .models import ViewSet
from .models import Attr
from .models import Anomaly
from .models import SampleSet
from .models import TrainTask


@admin.register(ViewSet, Attr, Anomaly, SampleSet, TrainTask)
class ViewSet(admin.ModelAdmin):
    pass


