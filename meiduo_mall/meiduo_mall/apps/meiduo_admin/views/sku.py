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
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator


class SKUInfoView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUModelSerializer

    @method_decorator(permission_required('goods.Goods_Sku'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
    @method_decorator(permission_required('goods.Goods_Sku'))
    def categories(self, request):
        goods = GoodsCategory.objects.filter(goodscategory=None)
        serializer = SKUThreeSerializer(goods, many=True)
        return Response(serializer.data)

    @method_decorator(permission_required('goods.Goods_Sku'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Sku'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Sku'))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Sku'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Sku'))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GoodsSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    @method_decorator(permission_required('goods.Goods_Sku'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GoodsSpecificationView(APIView):
    permission_classes = [IsAdminUser]

    @method_decorator(permission_required('goods.Goods_Specification'))
    def get(self, request, pk):
        goods = GoodsSpecification.objects.filter(spu_id=pk)
        serializer = GoodsSpecificationSerializer(goods, many=True)
        return Response(serializer.data)
