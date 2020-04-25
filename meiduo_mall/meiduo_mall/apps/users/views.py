import json
import re

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from django.views import View

# Create your views here.
from meiduo_mall.untils.JudgeLogin import LoginMixin
from users.models import User
from django.http import JsonResponse, HttpResponse
from django_redis import get_redis_connection


class UsernameCountView(View):

    def get(self, request, username):
        '''接受用户名,判断是否存在'''

        # 访问数据库
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '访问数据库失败'
            })

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'count': count
        })


class MobileCountView(View):
    '''手机号重复验证'''

    def get(self, request, mobile):
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '访问数据库失败'
            })
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'count': count
        })


class RegisterView(View):
    def post(self, request):
        '''注册接口'''
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        sms_code_client = dict.get('sms_code')
        allow = dict.get('allow')

        if not all([username, password, password2, mobile, sms_code_client, allow]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({
                'code': 400,
                'errmsg': '用户名格式不正确'
            })
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({
                'code': 400,
                'errmsg': '密码格式不正确'
            })
        if password2 != password:
            return JsonResponse({
                'code': 400,
                'errmsg': '两次输入密码不匹配'
            })
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': '手机号码格式不正确'
            })
        if not allow:
            return JsonResponse({
                'code': 400,
                'errmsg': '未勾选条款'
            })
        redis_coon = get_redis_connection('verify_code')
        sms_code_server = redis_coon.get('sms_%s' % mobile)
        if not sms_code_server:
            return JsonResponse({
                'code': 400,
                'errmsg': '短信验证码过期'
            })
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({
                'code': 400,
                'errmsg': '验证码不匹配'
            })

        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '存入数据库失败'
            })
        login(request, user)
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })


class LoginView(View):

    def post(self, request):
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')

        if not all([username, password]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必穿参数'
            })
        user = authenticate(username=username,
                            password=password)
        if user is None:
            return JsonResponse({'code': 400,
                                 'errmsg': '用户名或者密码错误'})
        login(request, user)

        if remembered is False:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        response = JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
        return response


class LogoutView(View):
    def delete(self, request):
        logout(request)
        response = JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })
        response.delete_cookie('username')
        return response


class UserInfoView(LoginMixin, View):
    def get(self, request):
        return HttpResponse('UserInfoView')
