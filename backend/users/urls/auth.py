from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import UserRegisterView, UserLoginView, VerifyCodeView

app_name = 'auth'

urlpatterns = [
    path('/register', UserRegisterView.as_view(), name='auth-register'),
    path('/login', UserLoginView.as_view(), name='auth-login'),
    path('/verify', VerifyCodeView.as_view(), name='auth-verify'),
    path('/refresh', TokenRefreshView.as_view(), name='auth-refresh'),
]
