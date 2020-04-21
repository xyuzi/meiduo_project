from django.shortcuts import render

# Create your views here.
from django.views import View

from captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse


class ImgcodeView(View):

    def get(self, request, uuid):
        '''生成图形验证码，保存redis后返回'''
        # 调用captcha框架生成图片和文本
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, 300, text)
        return HttpResponse(
            image,
            content_type='image/jpg'
        )
