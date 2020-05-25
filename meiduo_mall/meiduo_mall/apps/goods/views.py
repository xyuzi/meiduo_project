from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views import View

from goods.models import GoodsCategory, SKU, GoodsVisitCount
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


# 导入:
from haystack.views import SearchView


class MySearchView(SearchView):
    """重写SearchView类"""

    def create_response(self):
        page = self.request.GET.get('page')
        # 获取搜索结果
        context = self.get_context()
        data_list = []
        for sku in context['page'].object_list:
            data_list.append({
                'id': sku.object.id,
                'name': sku.object.name,
                'price': sku.object.price,
                'default_image_url': sku.object.default_image_url,
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count
            })
        # 拼接参数, 返回
        return JsonResponse(data_list, safe=False)


class DetailVisitView(View):
    def post(self, request, category_id):
        try:
            goods = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '数据库查询失败'
            })
        now = timezone.localdate()
        try:
            goods_visit = GoodsVisitCount.objects.get(date=now,
                                                      category_id=category_id)
        except Exception as e:
            goods_visit = GoodsVisitCount()
        try:

            goods_visit.category = goods
            goods_visit.count += 1
            goods_visit.save()
        except Exception as e:
            return JsonResponse({
                'code': 400,
                'errmsg': '数据库存储失败'
            })
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok'
        })
