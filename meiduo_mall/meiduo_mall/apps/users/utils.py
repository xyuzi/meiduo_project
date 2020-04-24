from django.contrib.auth.backends import ModelBackend
import re

from users.models import User


def get_user_or_mobile(account):
    '''判断是手机号还是用户名'''
    try:
        if re.match(r'^1[3-9]\d{9}', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except Exception as e:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        '''重写用户名认证，让其多出手机号登录'''
        user = get_user_or_mobile(username)
        if user and user.check_password(password):
            return user
