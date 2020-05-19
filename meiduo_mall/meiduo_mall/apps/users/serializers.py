from django_redis import get_redis_connection
from rest_framework import serializers
from django.http import Http404

from users.models import User


class UserSerializers(serializers.Serializer):
    password = serializers.CharField(label='密码', write_only=True, min_length=8, max_length=20)
    username = serializers.CharField(label='用户名')
    mobile = serializers.CharField(label='手机号', min_length=11, max_length=11)
    password2 = serializers.CharField(label='确认密码', write_only=True)
    allow = serializers.BooleanField(label='条款勾选', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)

    # def validate_password2(self, value):
    #     if not value:
    #         raise Exception('不能为空')
    #     return value
    #
    # def validate_sms_code(self, value):
    #     if not value:
    #         raise Exception('不能为空')
    #     return value
    #
    # def validated_allow(self, value):
    #     if not value:
    #         raise Exception('没有勾选条款')
    #     elif value:
    #         return value

    def validate(self, attrs):
        if attrs['password2'] != attrs['password']:
            raise Http404

        redis_coon = get_redis_connection('verify_code')
        try:
            sms_code_server = redis_coon.get('sms_%s' % attrs['mobile'])
        except Exception as e:
            raise Http404

        if not sms_code_server:
            raise Http404

        if attrs['sms_code'] != sms_code_server.decode():
            raise Http404

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],
                                        mobile=validated_data['mobile'])


class UserModolesSerializers(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = '__all__'
