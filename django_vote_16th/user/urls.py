from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import *

urlpatterns = [
    path('join/', JoinAPIView.as_view(), name='join'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify')
]