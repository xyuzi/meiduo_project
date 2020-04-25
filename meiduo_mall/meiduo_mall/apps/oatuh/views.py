from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.views import View


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
