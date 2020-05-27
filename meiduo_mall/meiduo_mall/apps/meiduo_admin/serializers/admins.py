from django.contrib.auth.models import Group
from rest_framework import serializers

from users.models import User


class AdminsModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'password']


class AdminSimplenModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
