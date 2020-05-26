from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from goods.models import SKU, GoodsCategory, Goods, GoodsSpecification
from meiduo_admin.serializers.sku import SKUModelSerializer, SKUSerializer, SKUThreeSerializer, GoodsSerializer, \
    GoodsSpecificationSerializer
from meiduo_admin.utils.pageresponse import PageNum


class SKUInfoView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUModelSerializer


class SKUView(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer
    pagination_class = PageNum

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')

        if keyword:
            return SKU.objects.filter(name=keyword)
        else:
            return SKU.objects.all()

    @action(detail=False)
    def categories(self, request):
        goods = GoodsCategory.objects.filter(goodscategory=None)
        serializer = SKUThreeSerializer(goods, many=True)
        return Response(serializer.data)


class GoodsSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer


class GoodsSpecificationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        goods = GoodsSpecification.objects.filter(spu_id=pk)
        serializer = GoodsSpecificationSerializer(goods, many=True)
        return Response(serializer.data)
