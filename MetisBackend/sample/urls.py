from django.urls import path
from . import api_views
from . import api_upload_views

app_name = "sample"

urlpatterns = [
    path('count/', api_views.SampleSetCountView.as_view(), name='count'),
    path('list/', api_views.SampleListView.as_view(), name='list'),
    path('delete/<pk>/', api_views.SampleDestroyView.as_view(), name='delete'),
    path('update/<pk>/', api_views.SampleUpdateView.as_view(), name='update'),
]

urlpatterns += [
    path('upload_list/', api_upload_views.UploadSampleListView.as_view(), name='upload_list'),
    path('upload_delete/<pk>/', api_upload_views.UploadSampleDestroyView.as_view(), name='upload_delete'),
    path('upload_file/<str:filename>/', api_upload_views.UploadSampleView.as_view(), name='upload_file'),
]
