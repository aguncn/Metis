from django.urls import path
from . import user_views

urlpatterns = [
    path('register/', user_views.UserRegisterView.as_view(), name='count'),
]