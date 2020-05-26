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


class GoodsBrandInfoView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GoodsBrandInfoSerializers
    queryset = Brand.objects.all()


class GoodsCategoriesOneInfoView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GoodsCategoryInfoSerializers
    queryset = GoodsCategory.objects.filter(parent_id=None)


class GoodsCategoriesInfoView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        goodsclass = GoodsCategory.objects.filter(parent_id=pk)
        serializer = GoodsCategoryInfoSerializers(goodsclass, many=True)
        return Response(serializer.data)
