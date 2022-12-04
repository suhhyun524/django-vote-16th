from django.urls import path

from .views import *

urlpatterns = [
    path('v1/test/', TestView.as_view(), name='test')
]