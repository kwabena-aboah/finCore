from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework import status
# from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from . models import Profile
from .serializers import UserSerliazer, ProfileSerializer
from django.core.exceptions import ObjectDoesNotExist

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
    

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.ObjectDoesNotExist:
            return Response({"error": "Profile not found"})
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=200)
    
    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.ObjectDoesNotExist:
            return Response({"error": "Profile not found"}, status=404)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200), 
        return Response(serializer.errors, status=400)