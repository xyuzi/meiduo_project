from rest_framework.generics import ListAPIView

from goods.models import SKU
from meiduo_admin.serializers import sku


class SKUInfoView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = sku.SKUModelSerializer
