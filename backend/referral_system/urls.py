from django.urls import path, include

from docs.redoc import doc_urlpatterns
from referral_system import settings

urlpatterns = [
    path('auth', include('users.urls.auth')),
    path('users', include('users.urls.users')),
]

if settings.DEBUG:
    urlpatterns += doc_urlpatterns
