from django.urls import path
from . import api_views

app_name = "anomaly"

urlpatterns = [
    path('list/', api_views.AnomalyListView.as_view(), name='list'),
    path('update/', api_views.AnomalyUpdateView.as_view(), name='update'),
]
