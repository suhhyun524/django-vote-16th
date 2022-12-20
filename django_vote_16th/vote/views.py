from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from user.models import User
from .serializers import TeamSerializer, UserSerializer, DemoVoteSerializer, PartVoteSerializer
from .models import Demo_Vote, PartLeader_Vote


# Create your views here.
class DemoVoteView(APIView):
    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="데모데이 팀 - 유저의 팀은 제외하고 리턴",
        operation_summary="데모데이",
        manual_parameters=[openapi.Parameter('Authorization',
                                             openapi.IN_HEADER,
                                             description="Authorization : Bearer {token}",
                                             type=openapi.TYPE_STRING)],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "team": openapi.Schema(description='투표할 수 있는 팀', type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def get(self, request):
        user_team = User.objects.get(user_id=request.user)
        lists = User.objects.all().exclude(team=user_team.team)
        serializer = TeamSerializer(lists, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="데모데이 투표",
        operation_summary="데모데이 투표",
        request_body=TeamSerializer,
        manual_parameters=[openapi.Parameter('Authorization',
                                             openapi.IN_HEADER,
                                             description="Authorization : Bearer {token}",
                                             type=openapi.TYPE_STRING)],
        responses={
            200: openapi.Schema(description="_팀에 투표 성공 or 이미 투표하셨습니다", type=openapi.TYPE_STRING),
        }
    )
    def post(self, request):
        user = User.objects.get(user_id=request.user)
        if not user.is_voted_demo:
            user.is_voted_demo = True
            user.save()
            Demo_Vote.objects.create(team=request.data['team'])
            msg = request.data['team']+"팀에 투표 성공"
        else:
            msg = "이미 투표하셨습니다"
        return Response(msg)


class PartVoteView(APIView):
    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="파트장",
        operation_summary="파트장",
        manual_parameters=[openapi.Parameter('Authorization',
                                             openapi.IN_HEADER,
                                             description="Authorization : Bearer {token}",
                                             type=openapi.TYPE_STRING)],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "name": openapi.Schema(description='파트원 이름', type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def get(self, request):
        user = User.objects.get(user_id=request.user)
        lists = User.objects.filter(part=user.part, is_candidate=True)
        serializer = UserSerializer(lists, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="파트장 투표",
        operation_summary="파트장 투표",
        request_body=UserSerializer,
        manual_parameters=[openapi.Parameter('Authorization',
                                             openapi.IN_HEADER,
                                             description="Authorization : Bearer {token}",
                                             type=openapi.TYPE_STRING)],
        responses={
            200: openapi.Schema(description="_에게 투표 성공 or 이미 투표하셨습니다", type=openapi.TYPE_STRING)
        }
    )
    def post(self, request):
        user = User.objects.get(user_id=request.user)
        if not user.is_voted_partleader:
            user.is_voted_partleader = True
            user.save()
            PartLeader_Vote.objects.create(part=user.part, votee=request.data['name'])
            msg = request.data['name']+"에게 투표 성공"
        else:
            msg = "이미 투표하셨습니다"
        return Response(msg)


class DemoResultView(APIView):
    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="데모 데이 투표 결과",
        operation_summary="데모 데이 투표 결과",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='내림차순 정렬',
                properties={
                    "team": openapi.Schema(description='팀 이름', type=openapi.TYPE_STRING),
                    "total": openapi.Schema(description='투표 수', type=openapi.TYPE_NUMBER)
                }
            )
        }
    )
    def get(self, request):
        lists = Demo_Vote.objects.all().values('team').annotate(total=Count('team')).order_by('-total')
        serializer = DemoVoteSerializer(lists, many=True)
        return Response(serializer.data)


class PartResultView(APIView):
    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="파트 리더 투표 결과",
        operation_summary="파트 리더 투표 결과",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='내림차순 정렬',
                properties={
                    "name": openapi.Schema(description='이름', type=openapi.TYPE_STRING),
                    "total": openapi.Schema(description='투표 수', type=openapi.TYPE_NUMBER)
                }
            )
        }
    )
    def get(self, request, part):
        lists = PartLeader_Vote.objects.filter(part=part).values('votee').annotate(total=Count('votee')).order_by('-total')
        serializer = PartVoteSerializer(lists, many=True)
        return Response(serializer.data)