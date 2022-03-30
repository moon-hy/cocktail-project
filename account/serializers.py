from rest_framework import serializers

from django.contrib.auth.models import User

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    id          = serializers.SerializerMethodField()
    name        = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'id', 'name', 'favorites', 'shelf',
        ]

    def get_id(self, obj):
        return obj.user.id

    def get_name(self, obj):
        return obj.user.username
