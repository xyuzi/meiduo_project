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

    @action(detail=False)
    def simple(self, request):
        spec = GoodsSpecification.objects.all()
        serializer = SpecsSipmpleModelSerializer(spec, many=True)
        return Response(serializer.data)
