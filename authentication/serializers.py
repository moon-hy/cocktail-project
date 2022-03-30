from rest_framework import serializers

from django.contrib.auth.models import User


class SignupSerializer(serializers.ModelSerializer):
    token       = serializers.SerializerMethodField()
    password    = serializers.CharField(
        max_length=255,
        min_length=8,
        write_only=True
    )

    class Meta:
        model   = User
        fields  = [
            'username', 'password', 'token',
        ]
        read_only_fields = ['token',]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_token(self, obj):
        return obj.auth_token.key

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model   = User
        fields  = [
            'id', 'username'
        ]


class UserSerializer(serializers.ModelSerializer):
    favorite    = serializers.SerializerMethodField()
    shelf       = serializers.SerializerMethodField()

    class Meta:
        model   = User
        fields  = [
            'username', 'favorite', 'shelf',
        ]

    def get_favorite(self, obj):
        return obj.account.favorite
    
    def get_shelf(self, obj):
        return obj.account.shelf
