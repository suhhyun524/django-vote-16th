from django.urls import path

from .views import *

urlpatterns = [
    path('', VoteView.as_view(), name='vote'),
    path('result/', ResultView.as_view(), name='result')
]