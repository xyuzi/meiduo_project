import base64
import json
import pickle

from django.http import JsonResponse
from django_redis import get_redis_connection
from django.shortcuts import render
# Create your views here.
from django.views import View

from goods.models import SKU


class CartsView(View):
    def post(self, request):
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        count = dict.get('count')
        selected = dict.get('selected', True)

        if not all([sku_id, count]):
            return JsonResponse({
                'code': 0,
                'errmsg': '缺少必传参数'
            })

        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({
                'code': 0,
                'errmsg': '查询数据失败'
            })
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({
                'code': 0,
                'errmsg': 'count参数出错'
            })

        if not isinstance(selected, bool):
            return JsonResponse({
                'code': 0,
                'errmsg': 'selected参数错误'
            })

        if request.user.is_authenticated:
            redis_conn = get_redis_connection('carts')

            pl = redis_conn.pipeline()

            pl.hincrby('carts_%s' % request.user.id,
                       sku_id,
                       count)
            pl.sadd('selects_%s' % request.user.id,
                    sku_id)

            pl.execute()

            return JsonResponse({
                'code': 0,
                'errmsg': 'ok'
            })
        else:
            cart_cookie = request.COOKIES.get('carts')
            if cart_cookie:
                cart_dict = pickle.loads(base64.b64decode(cart_cookie))
            else:
                cart_dict = {}

            if sku_id in cart_dict:
                count += cart_dict[sku_id]['count']

            cart_dict = base64.b64encode(pickle.dumps(cart_dict)).decode()

            response = JsonResponse({
                'code': 0,
                'errmsg': 'ok'
            })
            response.set_cookie('carts', cart_dict)

            return response

    def get(self, request):
        if request.user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            carts_dict = redis_conn.hgetall('carts_%s' % request.user.id)
            selects_dict = redis_conn.smembers('selects_%s' % request.user.id)
            cart_dict = {}
            for sku_id, count in carts_dict.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in selects_dict
                }
        else:
            cart_cookie = request.COOKIES.get('carts')
            if cart_cookie:
                cart_dict = pickle.loads(base64.b64decode(cart_cookie))
            else:
                cart_dict = {}

        sku_ids = cart_dict.keys()
        try:
            skus = SKU.objects.filter(id__in=sku_ids)
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '访问数据失败'
            })

        list = []
        for sku in skus:
            list.append({
                'id': sku.id,
                'name': sku.name,
                'count': cart_dict.get(sku.id).get('count'),
                'selected': cart_dict.get(sku.id).get('selected'),
                'default_image_url': sku.default_image_url,
                'price': sku.price,
                'amount': sku.price * cart_dict.get(sku.id).get('count'),
            })

        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'cart_skus': list})
