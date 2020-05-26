from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsSpecification
from meiduo_admin.serializers.specs import SpecsInfoModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class SpecsInfoView(ModelViewSet):
    pagination_class = PageNum
    serializer_class = SpecsInfoModelSerializer
    queryset = GoodsSpecification.objects.all()