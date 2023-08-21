from django.urls import path

from users.views import UserDetailView, ActivateInviteCodeView, UserListView

app_name = 'users'

urlpatterns = [
    path('/me', UserDetailView.as_view(), name='users-me'),
    path('/activate_invite_code', ActivateInviteCodeView.as_view(), name='users-activate-code'),
    path('/invited_by', UserListView.as_view(), name='users-invited-by')
]
