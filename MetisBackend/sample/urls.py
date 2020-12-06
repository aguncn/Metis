from django.urls import path
from . import api_views

urlpatterns = [
    path('count/', api_views.SampleSetCountView.as_view(), name='count'),
    path('list/', api_views.SampleListView.as_view(), name='list'),
    path('delete/<pk>/', api_views.SampleDestroyView.as_view(), name='delete'),
]
