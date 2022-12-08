from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('join/', JoinAPIView.as_view(), name='join'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login/refresh', TokenRefreshView.as_view(), name='token refresh')
]