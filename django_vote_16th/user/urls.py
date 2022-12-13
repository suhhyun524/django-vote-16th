from django.urls import path
from .views import *

urlpatterns = [
    path('join/', JoinAPIView.as_view(), name='join'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyAPIView.as_view(), name='token_verify'),
    path('logout/', LogoutAPIView.as_view(), name='logout')
]