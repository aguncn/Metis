from django.urls import path
from . import user_views

app_name = "account"

urlpatterns = [
    path('register/', user_views.UserRegisterView.as_view(), name='register'),
    path('update_password/', user_views.UpdatePasswordView.as_view(), name='update_password'),
    path('update_email/', user_views.UpdateEmailView.as_view(), name='update_email'),
    path('forget_password/', user_views.ForgetPasswordView.as_view(), name='forget_password'),
    path('reset_password/', user_views.ResetPasswordView.as_view(), name='reset_password'),
]
