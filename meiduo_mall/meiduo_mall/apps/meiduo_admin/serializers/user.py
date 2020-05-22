from rest_framework import serializers

from users.models import User


class UserInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email']
