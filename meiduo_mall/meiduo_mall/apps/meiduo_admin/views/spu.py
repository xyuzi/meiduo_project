from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from goods.models import Goods, Brand, GoodsCategory
from meiduo_admin.serializers.spu import GoodsInfoSerializers, GoodsBrandInfoSerializers, GoodsCategoryInfoSerializers
from meiduo_admin.utils.pageresponse import PageNum


class GoodsInfoView(ModelViewSet):
    permission_classes = [IsAdminUser]
    pagination_class = PageNum
    serializer_class = GoodsInfoSerializers
    queryset = goods = Goods.objects.all()

    # @method_decorator(permission_required('goods.Goods_spu'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @method_decorator(permission_required('goods.Goods_spu'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_spu'))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_spu'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_spu'))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GoodsBrandInfoView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GoodsBrandInfoSerializers
    queryset = Brand.objects.all()

    # @method_decorator(permission_required('goods.Goods_spu'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GoodsCategoriesOneInfoView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GoodsCategoryInfoSerializers
    queryset = GoodsCategory.objects.filter(parent_id=None)

    # @method_decorator(permission_required('goods.Goods_Category'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GoodsCategoriesInfoView(APIView):
    permission_classes = [IsAdminUser]

    @method_decorator(permission_required('goods.Goods_Category'))
    def get(self, request, pk):
        goodsclass = GoodsCategory.objects.filter(parent_id=pk)
        serializer = GoodsCategoryInfoSerializers(goodsclass, many=True)
        return Response(serializer.data)
