from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.views import View
import logging

from oatuh.models import OAuthQQUser
from oatuh.utils import generate_access_token_by_openid

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
            auth_qq = OAuthQQUser.object.get(openid=openid)
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
