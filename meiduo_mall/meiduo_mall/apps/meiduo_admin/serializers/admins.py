from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from users.models import User


class AdminsModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    mobile = serializers.CharField(max_length=11, min_length=11)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'password', 'groups', 'user_permissions']


class AdminSimplenModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
