from django.shortcuts import render

# Create your views here.
from django.views import View

from captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse, JsonResponse
from yuntongxun.ccp_sms import CCP
import logging
import random

logger = logging.getLogger('django')


class ImgcodeView(View):

    def get(self, request, uuid):
        '''生成图形验证码，保存redis后返回'''
        # 调用captcha框架生成图片和文本
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_code')
        # 存入uuid
        redis_conn.setex('img_%s' % uuid, 300, text)
        return HttpResponse(
            image,
            content_type='image/jpg'
        )


class SMSCodeView(View):

    def get(self, request, mobile):
        # 获取传入参数 验证码，之前存入的uuid
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        # 创建redis链接对象
        redis_conn = get_redis_connection('verify_code')
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return JsonResponse({
                'code': 400,
                'errmsg': '发送短信过于频繁'
            })

        if not all([image_code_client, uuid]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })
        # 获取uid对应的value(二进制)
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return JsonResponse({
                'code': 400,
                'errmsg': '图形验证码失效'
            })
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)
        # 判断验证码是否正确
        if image_code_client.lower() != image_code_server.decode().lower():
            return JsonResponse({
                'code': 400,
                'errmsg': '输入图形验证码有误'
            })
        sms_code = '%06d' % random.randint(1, 999999)
        # 日志输出验证码
        logger.info(sms_code)
        # 管道创建
        p1 = redis_conn.pipeline()
        # redis保存电话与验证码，保存倒计时时间
        p1.setex('sms_%s' % mobile, 300, sms_code)
        p1.setex('send_flag_%s' % mobile, 300, 1)

        # 管道执行
        p1.execute()

        # 发送短信
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        return JsonResponse({
            'code': 0,
            'errmsg': '发送短信验证码成功'
        })
