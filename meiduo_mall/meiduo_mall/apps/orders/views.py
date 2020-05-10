import json
from decimal import Decimal

from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views import View
from django.http import JsonResponse
from django.db import transaction

from carts.models import OrderInfo, OrderGoods
from goods.models import SKU, Goods
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


class OrderCommitView(LoginMixin, View):

    def post(self, request):
        dict = json.loads(request.body.decode())

        address_id = dict.get('address_id')
        pay_method = dict.get('pay_method')

        if not all([address_id, pay_method]):
            return JsonResponse({
                'code': 400,
                'errmsg': '缺少必传参数'
            })

        try:
            address = Address.objects.get(id=address_id)
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '传入地址有误'
            })

        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return JsonResponse({
                'code': 400,
                'errmsg': '传入支付方式有误'
            })

        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % request.user.id)
        with transaction.atomic():

            save_id = transaction.savepoint()

            order = OrderInfo.objects.create(
                order_id=order_id,
                user=request.user,
                address=address,
                total_count=0,
                total_amount=Decimal('0.00'),
                freight=Decimal('10.00'),
                pay_method=pay_method,
                status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method in [
                    OrderInfo.PAY_METHODS_ENUM['ALIPAY']] else
                OrderInfo.ORDER_STATUS_ENUM['UNSEND']
            )

            redis_conn = get_redis_connection('carts')

            carts_dict = redis_conn.hgetall('carts_%s' % request.user.id)
            selects_list = redis_conn.smembers('selects_%s' % request.user.id)

            dict = {}

            for sku_id in selects_list:
                dict[int(sku_id)] = int(carts_dict[sku_id])

            for sku_id in dict.keys():
                while True:
                    sku = SKU.objects.get(id=sku_id)
                    goods = sku.goods
                    goods_sales = goods.sales
                    stock = sku.stock
                    sales = sku.sales

                    sku_count = dict[sku.id]

                    if sku_count > sku.stock:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({
                            'code': 400,
                            'errmsg': '库存不足'
                        })

                    new_stock = stock - sku_count
                    new_sales = sales + sku_count
                    new_goods = goods_sales + sku_count
                    # sku.stock -= sku_count
                    # sku.sales += sku_count
                    # sku.save()

                    result = SKU.objects.filter(id=sku_id, stock=stock).update(stock=new_stock, sales=new_sales)
                    if result == 0:
                        continue

                    # sku.goods.sales += sku_count
                    # sku.goods.save()

                    result = Goods.objects.filter(id=sku.goods_id).update(sales=new_goods)
                    if result == 0:
                        continue

                    OrderGoods.objects.create(
                        order=order,
                        sku=sku,
                        count=sku_count,
                        price=sku.price
                    )

                    order.total_count += sku_count
                    order.total_amount += (sku_count * sku.price)

                    break

            transaction.savepoint_commit(save_id)

            order.total_amount += order.freight
            order.save()

        pl = redis_conn.pipeline()

        pl.hdel('carts_%s' % request.user.id, *selects_list)
        pl.srem('selects_%s' % request.user.id, *selects_list)

        pl.execute()

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'order_id': order.order_id
        })
