from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

class TestView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response("Swagger 연동 테스트")