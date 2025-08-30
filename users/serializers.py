from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    
    
    user = serializers.HyperlinkedRelatedField(read_only = True, many=False, view_name='user-detail')
    
    class Meta:
        model = Profile
        fields = ['url','id','user','image']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True)
    profile = ProfileSerializer(read_only=True)  # Nested serializer for Profile, read-only
    #validate password
    def validate(self, value):
        request_method = self.context['request'].method
        password = value.get('password')
        old_password = value.get('old_password')    
        if request_method == 'POST':
            if not password:
                raise serializers.ValidationError({"password": "Password is required for creating a user."})
        elif request_method in ['PUT', 'PATCH']:
            if password and not old_password:
                raise serializers.ValidationError({"old_password": "Old password is required to set a new password."})
        return value
    
    
    
    
    
    
    
    #create user with hashed password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        user = instance
        password = validated_data.pop('password', None)
        old_password = validated_data.pop('old_password', None)


        # If a new password is provided, old_password must be correct
        if "password" in validated_data:
            if not old_password:
                raise serializers.ValidationError({"old_password": "Old password is required to set a new password."})
            if not user.check_password(old_password):
                raise serializers.ValidationError({"old_password": "Old password is incorrect."})
            user.set_password(password)
            user.save()

        # Update other fields
        return super().update(user, validated_data)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'password', 'old_password', 'profile']
