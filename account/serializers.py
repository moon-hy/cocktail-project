from rest_framework import serializers

from django.contrib.auth.models import User

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    name        = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'name', 'favorites', 'shelf',
        ]
        
    def get_name(self, obj):
        return obj.user.username
