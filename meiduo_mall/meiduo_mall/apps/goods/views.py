from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views import View

from goods.models import GoodsCategory, SKU
from django.http import JsonResponse
import logging

from goods.utiles import get_breadcrumb

logger = logging.getLogger('django')


class ListView(View):

    def get(self, request, category_id):
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        ordering = request.GET.get('ordering')

        try:
            category = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '根据ID获取数据失败'
            })

        try:
            skus = SKU.objects.filter(category=category,
                                      is_launched=True).order_by(ordering)
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '根据category获取数据失败'
            })

        paginator = Paginator(skus, page_size)
        try:
            page_skus = paginator.page(page)
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '传入页码有误'
            })
        totoal = paginator.num_pages
        list = []
        for sku in page_skus:
            list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image_url,
                'price': sku.price
            })
        breadcrumb = get_breadcrumb(category)

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'breadcrumb': breadcrumb,
            'list': list,
            'count': totoal
        })


class HotGoodsView(View):
    def get(self, request, category_id):
        try:
            skus = SKU.objects.filter(category_id=category_id,
                                      is_launched=True).order_by('-sales')[:2]
        except Exception as e:
            logger.info(e)
            return JsonResponse({
                'code': 400,
                'errmsg': '从数据库获取数据失败'
            })

        list = []

        for sku in skus:
            list.append({
                'id': sku.id,
                'default_image_url': sku.default_image_url,
                'price': sku.price,
                'name': sku.name
            })

        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'hot_skus': list
        })
