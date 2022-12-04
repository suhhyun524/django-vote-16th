from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from api.models import *
from .open_api_params import *


# Create your views here.
class VoteView(APIView):
    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema(manual_parameters=get_params)
    def get(self, request):
        return Response("Swagger 연동 테스트")

    @swagger_auto_schema(manual_parameters=post_params)
    def post(self, request):
        return Response("Swagger post 테스트")