from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse

from goods.models import SKU
from meiduo_mall.utils.JudgeLogin import LoginMixin
from users.models import Address
from django_redis import get_redis_connection


class OrderSettlementView(LoginMixin, View):

    def get(self, request):
        try:
            addresses = Address.objects.filter(user=request.user,
                                               is_delete=False)
        except Exception as e:
            addresses = None
        address_list = []
        for address in addresses:
            address_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'receiver': address.receiver
            })
        redis_conn = get_redis_connection('carts')

        carts_dict = redis_conn.hgetall('carts_%s' % request.user.id)
        selects_list = redis_conn.smembers('selects_%s' % request.user.id)

        sku_ids = {}
        for sku_id in selects_list:
            sku_ids[int(sku_id)] = int(carts_dict[sku_id])

        try:
            skus = SKU.objects.filter(id__in=sku_ids.keys())
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '查找商品错误'
            })

        sku_list = []
        for sku in skus:
            sku_list.append({
                "id": sku.id,
                "name": sku.name,
                "default_image_url": sku.default_image_url,
                "count": sku_ids[sku.id],
                "price": sku.price,
            })

        context = {
            'addresses': address_list,
            'skus': sku_list,
            "freight": 10,
        }

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'context': context
        })
