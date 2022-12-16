from django.urls import path

from .views import *

urlpatterns = [
    path('demo/', DemoVoteView.as_view(), name='demo-vote'),
    path('part/', PartVoteView.as_view(), name='part-vote'),
    path('result/demo/', DemoResultView.as_view(), name='result'),
    path('result/part/<str:part>', PartResultView.as_view(), name='result')
]