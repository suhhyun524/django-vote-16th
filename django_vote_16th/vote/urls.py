from django.urls import path

from .views import *

urlpatterns = [
    path('v1/vote/', VoteView.as_view(), name='vote')
]