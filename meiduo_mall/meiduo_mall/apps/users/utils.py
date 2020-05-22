from django.contrib.auth.backends import ModelBackend
import re

from users.models import User


def get_user_or_mobile(account):
    """判断是手机号还是用户名"""
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
        """重写用户名认证，让其多出手机号登录"""
        user = get_user_or_mobile(username)
        if request is None:  # 判断是否传入request区分登录客户端
            # 判断查询到的user是不是超级用户,检查密码
            if user.is_superuser and user.check_password(password):
                return user
        else:
            # 判断是否查询到user,检查密码
            if user and user.check_password(password):
                return user
