from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import *
from .models import *

# 회원가입
class JoinAPIView(APIView):

    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="회원 가입",
        operation_summary="회원 가입 API",
        request_body=JoinSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "user_id": openapi.Schema(description='회원 id', type=openapi.TYPE_STRING),
                            "name": openapi.Schema(description='회원 이름', type=openapi.TYPE_STRING),
                            "part": openapi.Schema(description='회원이 속한 파트', type=openapi.TYPE_STRING),
                            "team": openapi.Schema(description='회원이 속한 팀', type=openapi.TYPE_STRING),
                        }
                    ),
                    "message": openapi.Schema(description='회원가입 여부', type=openapi.TYPE_STRING),
                    "token": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "access": openapi.Schema(description='access token', type=openapi.TYPE_STRING),
                            "refresh": openapi.Schema(description='refresh token', type=openapi.TYPE_STRING),
                        }
                    ),
                }
            )
        }
    )

    def post(self, request):
        serializer = JoinSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근해주기
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": {
                        "user_id": serializer.data.get("user_id"),
                        "name": serializer.data.get("name"),
                        "part": serializer.data.get("part"),
                        "team": serializer.data.get("team")
                    },
                    "message": "회원가입 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema()
    def get(self, request):
        return Response("Swagger 연동 테스트")