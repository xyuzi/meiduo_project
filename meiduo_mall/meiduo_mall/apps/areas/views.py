from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from areas.models import Area
from django.core.cache import cache
import logging

logger = logging.getLogger('django')


class ProvinceAreasView(View):
    """省级地区"""

    def get(self, request):
        province_list = cache.get('province_list')
        if not province_list:
            logger.info('进入省存储缓存')
            try:
                province_models_list = Area.objects.filter(parent__isnull=True)
                province_list = []
                for province_models in province_models_list:
                    province_list.append({
                        'id': province_models.id,
                        'name': province_models.name
                    })
                cache.set('province_list', province_list, 3600)
            except Exception as e:
                return JsonResponse({
                    'code': 400,
                    'errmsg': '数据库查询错误'
                })
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'province_list': province_list
        })


class SubAreasView(View):
    """市级区域"""

    def get(self, request, pk):
        sub_data = cache.get('sub_' + pk)
        if not sub_data:
            logger.info('进入市存储缓存')
            try:
                sub_models_list = Area.objects.filter(parent=pk)
                parent = Area.objects.get(id=pk)
                sub_list = []
                for sub_models in sub_models_list:
                    sub_list.append({
                        'id': sub_models.id,
                        'name': sub_models.name
                    })
                sub_data = {
                    'id': parent.id,
                    'name': parent.name,
                    'subs': sub_list
                }
                cache.set('sub_' + pk, sub_data, 3600)
            except Exception as e:
                logger.info(e)
                return JsonResponse({
                    'code': 400,
                    'errmsg': '数据库查询错误'
                })
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'sub_data': sub_data
        })
