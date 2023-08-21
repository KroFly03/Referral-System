from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

doc_urlpatterns = [
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
