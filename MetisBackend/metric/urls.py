from django.urls import path
from . import api_view_set_views
from . import api_attr_views

app_name = "metric"

urlpatterns = [
    path('view_set_list/', api_view_set_views.ViewSetListView.as_view(), name='view_set_list'),
    path('view_set_create/', api_view_set_views.ViewSetCreateView.as_view(), name='view_set_create'),
    path('view_set_delete/<pk>/', api_view_set_views.ViewSetDestroyView.as_view(), name='view_set_delete'),
    path('view_set_update/<pk>/', api_view_set_views.ViewSetUpdateView.as_view(), name='view_set_update'),
]

urlpatterns += [
    path('attr_list/', api_attr_views.AttrListView.as_view(), name='attr_list'),
    path('attr_create/', api_attr_views.AttrCreateView.as_view(), name='attr_create'),
    path('attr_delete/<pk>/', api_attr_views.AttrDestroyView.as_view(), name='attr_delete'),
    path('attr_update/<pk>/', api_attr_views.AttrUpdateView.as_view(), name='attr_update'),
]
