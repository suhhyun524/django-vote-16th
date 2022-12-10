from django.urls import path

from .views import *

urlpatterns = [
    path('join/', JoinAPIView.as_view(), name='join'),
    path('login/', LoginAPIView.as_view(), name='login')
]