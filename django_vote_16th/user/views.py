from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, \
    TokenVerifySerializer
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import *
from .models import *

# 회원가입
class JoinAPIView(APIView):

    permissions_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="회원 가입",
        operation_summary="회원 가입",
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
                            "is_candidate": openapi.Schema(description='후보자 여부', type=openapi.TYPE_BOOLEAN)
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
                        "team": serializer.data.get("team"),
                        "is_candidate": serializer.data.get("is_candidate"),
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

    @swagger_auto_schema(
        operation_description="로그인",
        operation_summary="로그인",
        request_body=LoginSerializer,
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
                    "message": openapi.Schema(description='로그인 여부', type=openapi.TYPE_STRING),
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
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = User.objects.get(user_id=serializer.validated_data)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            user.refresh_token = refresh_token
            user.save()
            res = Response(
                {
                    "user": {
                        "user_id": user.user_id,
                        "name": user.name,
                        "part": user.part,
                        "team": user.team
                    },
                    "message": "로그인 성공",
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


# 토큰 재발급
class TokenRefreshAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="access token 재발급",
        operation_summary="access token 재발급",
        request_body=TokenRefreshSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(description="access token 재발급 성공", type=openapi.TYPE_STRING),
                    "token": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "access": openapi.Schema(description='access token', type=openapi.TYPE_STRING),
                        }
                    ),
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(description="refresh token이 유효하지 않거나 만료되었습니다.", type=openapi.TYPE_STRING),
                }
            )
        }
    )

    def post(self, request):
        try:
            # access 토큰 만료시
            serializer = TokenRefreshSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                access_token = serializer.validated_data['access']
                refresh_token = request.COOKIES.get('refresh_token', None)
                res = Response(
                    {
                        "message": "access token 재발급 성공",
                        "token": {
                            "access": access_token,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
                res.set_cookie('access_token', access_token, httponly=True)
                res.set_cookie('refresh_token', refresh_token, httponly=True)
                print(access_token)
                return res
        except(TokenError):  # refresh 토큰까지 만료 시
            return Response({"message": "refresh token이 유효하지 않거나 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 토큰 유효성 검사
class TokenVerifyAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="토큰 유효성 검사",
        operation_summary="토큰 유효성 검사",
        request_body=TokenVerifySerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(description='유효한 토큰입니다.', type=openapi.TYPE_STRING)
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(description="유효하지 않거나 만료된 토큰입니다.", type=openapi.TYPE_STRING)
                }
            )
        }
    )

    def post(self, request):
        try:
            serializer = TokenVerifySerializer(data=request.data)

            if serializer.is_valid(raise_exception=False):
                res = Response(
                    {
                        "message": "유효한 토큰입니다.",
                    },
                    status=status.HTTP_200_OK,
                )
                return res

        except(TokenError):  # 토큰 만료 시
            return Response({"message": "토큰이 유효하지 않거나 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃
class LogoutAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="로그아웃",
        operation_summary="로그아웃",
        request_body=LogoutSerializer,
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
                    "message": openapi.Schema(description='로그아웃 여부', type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid(raise_exception=False):
            user = User.objects.get(user_id=serializer.validated_data)
            user.refresh_token = None
            user.save()
            res = Response(
                {
                    "user": {
                        "user_id": user.user_id,
                        "name": user.name,
                        "part": user.part,
                        "team": user.team
                    },
                    "message": "로그아웃 성공",
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)