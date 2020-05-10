from django.shortcuts import render
import os

# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.conf import settings

from carts.models import OrderInfo
from alipay import AliPay

from payment.models import Payment


class PaymentView(View):

    def get(self, request, order_id):

        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=request.user,
                                          status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '传入order_id有误'
            })

        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "keys/alipay_public_key.pem"),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject="美多商城%s" % order_id,
            return_url=settings.ALIPAY_RETURN_URL,
        )

        alipay_url = settings.ALIPAY_URL + '?' + order_string
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'alipay_url': alipay_url
        })


# /payment/status/?
# charset=utf-8&
# out_trade_no  # 订单编号
# method=alipay.trade.page.pay.return&
# total_amount=3798.00&
# sign=KzyOwZWOOgdX5AsxuLl5uiTloG9amvFB%2BjmXqEmznPHviCBe0rVjks0m6ULZfuJStiDSND0aF7AsdApyyerXbkhjpwzSCMBaSAvECdqpaKZ4%2BM0kn05OyD7FEpYRY4TWR02EutrEQHRC6kTCK4QLoQUC%2BaGYxqopZ7BqI0O1%2Bhme61aYoVACmK3dVH0GbXoNRCHxGif686iaSbuaUlKFRpGH6C9hN88vS8z5AMDkMHtOvuzvjYFVoe%2B17ZTc2NWiFIOFX%2BE9kV7LMFw4%2Fqm2hSKPIXfNJgFpZOPoIQMrbIaqlSif7VSpf0xYMu2%2FPSWvHbACcdDZ2wV6VMiL%2Bg2I9Q%3D%3D&
# trade_no= # 流水号
# auth_app_id=2016102200739447&version=1.0&
# app_id=2016102200739447&
# sign_type=RSA2&
# seller_id=2088102180659002&
# timestamp=2020-05-10+10%3A47%3A16
# HTTP/1.1

class PaymentStatusView(View):

    def put(self, request):
        qdict = request.GET
        dict = qdict.dict()

        sig = dict.pop('sign')

        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "keys/alipay_public_key.pem"),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )

        success = alipay.verify(dict, sig)
        if success:
            try:
                order_id = dict.get('out_trade_no')
                trade_id = dict.get('trade_no')
                Payment.objects.create(
                    order_id=order_id,
                    trade_id=trade_id
                )
                OrderInfo.objects.filter(order_id=order_id,
                                         status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                    status=OrderInfo.ORDER_STATUS_ENUM["UNRECEIVED"])
                return JsonResponse({
                    'code': 0,
                    'errmsg': 'ok',
                    'trade_id': trade_id
                })
            except Exception as e:
                return JsonResponse({
                    'code': 400,
                    'errmsg': '保存失败'
                })
        else:
            return JsonResponse({
                'code': 400,
                'errmsg': '非法请求'
            })
