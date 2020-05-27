from rest_framework import serializers

from django.contrib.auth.models import Group, Permission


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class SimplenModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name']
