from django.contrib.auth.models import User
from rest_framework import serializers
from . models import Profile

class UserSerliazer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'phone']
        read_only_fields = ['id', 'user']