from django.urls import path
from . import api_views

urlpatterns = [
    path('list/', api_views.AnomalyListView.as_view(), name='list'),
]
