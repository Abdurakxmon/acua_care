# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone', 'address']

class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data['username'] = validated_data['email']

        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.create(user=user, **profile_data)

        return user

