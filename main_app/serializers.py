from rest_framework import serializers
from .models import Interest, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class InterestSerializer(serializers.ModelSerializer):
    user= serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model=Interest
        fields='__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields='__all__'
        read_only_fields=('interest',)