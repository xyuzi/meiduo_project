import json
import re

from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.views import View
import logging
from django_redis import get_redis_connection

from carts.utiles import merage_cookie
from oatuh.models import OAuthQQUser
from oatuh.utils import generate_access_token_by_openid, check_access_token_by_openid
from users.models import User

logger = logging.getLogger('django')


class QqUrlView(View):
    '''返回QQ网址'''

    def get(self, request):
        next = request.GET.get('next')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        url = oauth.get_qq_url()
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'login_url': url
        })


class QqUrlSecondView(View):

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return JsonResponse({
                'code': 400,
                'errmsg': '必传参数为空'
            })
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        )
        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '获取openid失败'
            })

        try:
            auth_qq = OAuthQQUser.objects.get(openid=openid)
        except:
            access_token = generate_access_token_by_openid(openid)
            return JsonResponse({
                'code': 300,
                'errmsg': 'ok',
                'access_token': access_token
            })
        else:
            user = auth_qq.user
            login(request, user)
            response = JsonResponse({
                'code': 0,
                'errmsg': 'ok'
            })
            response.set_cookie('username',
                                user.username,
                                max_age=3600 * 24 * 14)
            return response

    def post(self, request):
        dict = json.loads(request.body.decode())
        mobile = dict.get('mobile')
        password = dict.get('password')
        sms_code_client = dict.get('sms_code')
        access_token = dict.get('access_token')

        if not all([mobile, password, sms_code_client, access_token]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({
                'code': 400,
                'errmsg': '手机号格式错误'
            })

        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({
                'code': 400,
                'errmsg': '密码格式错误'
            })
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
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
        openid = check_access_token_by_openid(access_token)
        if not openid:
            return JsonResponse({
                'code': 400,
                'errmsg': 'openid验证失败'
            })

        try:
            user = User.objects.get(mobile=mobile)
        except Exception as e:
            user = User.objects.create_user(username=mobile,
                                            password=password,
                                            mobile=mobile)
        else:
            if not user.check_password(password):
                return JsonResponse({
                    'code': 400,
                    'errmsg': '密码匹配失败'
                })
        try:
            OAuthQQUser.objects.create(openid=openid,
                                       user=user)
        except:
            return JsonResponse({
                'code': 400,
                'errmsg': '存入QQ表失败'
            })
        login(request, user)
        response = JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })
        response.set_cookie('username', user.username,
                            max_age=3600 * 24 * 14)

        response = merage_cookie(request, response)
        return response
