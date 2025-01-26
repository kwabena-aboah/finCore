from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerliazer

class RegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerliazer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response(UserSerliazer(user).data, status=status.HTTP_201_CREATED)