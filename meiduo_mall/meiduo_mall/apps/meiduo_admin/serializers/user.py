from rest_framework import serializers

from users.models import User


class UserInfoModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20, min_length=5)
    password = serializers.CharField(max_length=20, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
