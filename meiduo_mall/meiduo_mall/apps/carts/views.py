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
            cart_data = request.COOKIES.get('carts')
            if cart_data:
                cart_dict = pickle.loads(base64.b64decode(cart_data.encode()))
            else:
                cart_dict = {}

            if sku_id in cart_dict:
                count += cart_dict[sku_id]['count']

            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }

            cart_dict = base64.b64encode(pickle.dumps(cart_dict)).decode()

            response = JsonResponse({
                'code': 0,
                'errmsg': 'ok'
            })
            response.set_cookie('carts', cart_dict, max_age=3600 * 24 * 14)

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

    def put(self, request):
        """修改购物车"""
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        count = dict.get('count')
        selected = dict.get('selected', True)

        if not all([sku_id, count]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '传入count错误'
            })

        if selected:
            if not isinstance(selected, bool):
                return JsonResponse({
                    'code': 400,
                    'errmsg': '传入selected错误'
                })
        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '传入sku编号有误'
            })

        if request.user.is_authenticated:
            redis_conn = get_redis_connection('carts')

            pl = redis_conn.pipeline()

            pl.hset('carts_%s' % request.user.id, sku_id, count)

            if selected:
                pl.sadd('selects_%s' % request.user.id, sku_id)
            else:
                pl.srem('selects_%s' % request.user.id, sku_id)

            pl.execute()

            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'default_image_url': sku.default_image_url,
                'price': sku.price,
                'amount': sku.price * count
            }
            return JsonResponse({
                'code': 0,
                'errmsg': 'ok',
                'cart_sku': cart_sku
            })

        else:
            cookies_carts = request.COOKIES.get('carts')
            if cookies_carts:
                cart_dict = pickle.loads(base64.b64decode(cookies_carts.encode()))
            else:
                return JsonResponse({
                    'code': 400,
                    'errmsg': '修改数据不存在'
                })

            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            cart_data = base64.b64encode(pickle.dumps(cart_dict)).decode()

            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected
            }

            response = JsonResponse({
                'code': 0,
                'errmsg': 'ok',
                'cart_sku': cart_sku
            })
            response.set_cookie('carts', cart_data, max_age=3600 * 24 * 14)

            return response

    def delete(self, request):
        dict = json.loads(request.body.decode())
        sku_id = dict.get('sku_id')
        if not sku_id:
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })
        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '传入sku错误'
            })

        if request.user.is_authenticated:
            redis_conn = get_redis_connection('carts')

            pl = redis_conn.pipeline()

            pl.hdel('carts_%s' % request.user.id, sku_id)
            pl.srem('selects_%s' % request.user.id, sku_id)

            pl.execute()

            return JsonResponse({
                'code': 0,
                'errmsg': 'ok'
            })
        else:
            carts_data = request.COOKIES.get('carts')

            if carts_data:
                carts_dict = pickle.loads(base64.b64decode(carts_data))
            else:
                return JsonResponse({
                    'code': 400,
                    'errmsg': '删除数据不存在'
                })

            if sku_id in carts_dict:
                # del carts_dict[sku_id]
                carts_dict.pop(sku_id)

                carts_data = base64.b64encode(pickle.dumps(carts_dict)).decode()

                response = JsonResponse({
                    'code': 0,
                    'errmsg': 'ok'
                })

                response.set_cookie('carts', carts_data, max_age=3600 * 24 * 14)

                return response


class Selectcarts(View):
    def put(self, request):
        dict = json.loads(request.body.decode())
        selected = dict.get('selected', True)

        if not isinstance(selected, bool):
            return JsonResponse({
                'code': 400,
                'errmsg': '传入值类型错误'
            })

        if request.user.is_authenticated:
            redis_conn = get_redis_connection('carts')

            carts_dict = redis_conn.hgetall('carts_%s' % request.user.id)

            selected_list = carts_dict.keys()

            if selected:
                redis_conn.sadd('selects_%s' % request.user.id, *selected_list)
            else:
                redis_conn.srem('selects_%s' % request.user.id, *selected_list)

            return JsonResponse({
                'code': 0,
                'errmsg': 'ok'
            })

        else:
            carts_data = request.COOKIES.get('carts')

            if carts_data:
                carts_dict = pickle.loads(base64.b64decode(carts_data))

                for carts_key in carts_dict.keys():
                    carts_dict[carts_key] = selected

                response = JsonResponse({
                    'code': 0,
                    'errmsg': 'ok'
                })
                carts_data = base64.b64encode(pickle.dumps(carts_dict))

                response.set_cookie('carts', carts_data, max_age=3600 * 24 * 14)

                return response
            else:
                return JsonResponse({
                    'code': 400,
                    'errmsg': '操作异常'
                })
