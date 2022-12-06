from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from api.models import User
from api.serializers import TeamSerializer, UserSerializer
from .models import Demo_Vote, PartLeader_Vote

from .open_api_params import *


# Create your views here.
class DemoVoteView(APIView):
    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema()
    def get(self, request):
        lists = User.objects.all()
        serializer = TeamSerializer(lists, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(request_body=demo_vote)
    def post(self, request):

        # if(user_team!=request.data['team'])
        Demo_Vote.objects.create(team=request.data['team'])

        return Response("데모 데이 투표 성공")


class PartVoteView(APIView):
    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema(manual_parameters=part_get)
    def get(self, request, part):
        lists = User.objects.filter(part=part)
        serializer = UserSerializer(lists, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(request_body=part_vote)
    def post(self, request, part):
        # if user_part==part
        PartLeader_Vote.objects.create(part=part, votee=request.data['votee'])

        return Response("파트 리더 투표 성공")


class DemoResultView(APIView):
    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema()
    def get(self, request):
        lists = Demo_Vote.objects.all().values('team').annotate(total=Count('team')).order_by('-total')
        return Response(lists)


class PartResultView(APIView):
    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema()
    def get(self, request, part):
        lists = PartLeader_Vote.objects.filter(part=part).values('votee').annotate(total=Count('votee')).order_by('-total')
        return Response(lists)
