from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsSpecification
from meiduo_admin.serializers.specs import SpecsInfoModelSerializer, SpecsSipmpleModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class SpecsInfoView(ModelViewSet):
    permission_classes = [IsAdminUser]
    pagination_class = PageNum
    serializer_class = SpecsInfoModelSerializer
    queryset = GoodsSpecification.objects.all()

    # @method_decorator(permission_required('goods.Goods_Specification'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @method_decorator(permission_required('goods.Goods_Specification'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Specification'))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Specification'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Specification'))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False)
    # @method_decorator(permission_required('goods.Goods_Specification'))
    def simple(self, request):
        spec = GoodsSpecification.objects.all()
        serializer = SpecsSipmpleModelSerializer(spec, many=True)
        return Response(serializer.data)
