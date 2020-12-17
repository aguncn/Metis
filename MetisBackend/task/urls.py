from django.urls import path
from . import api_views

urlpatterns = [
    path('list/', api_views.TaskListView.as_view(), name='list'),
    path('create/', api_views.TaskCreateView.as_view(), name='create'),
    path('delete/<pk>/', api_views.TaskDestroyView.as_view(), name='delete'),
    path('model_list/', api_views.ModelListView.as_view(), name='model_list'),
]
