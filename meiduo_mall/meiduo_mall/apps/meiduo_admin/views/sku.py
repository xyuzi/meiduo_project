from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from goods.models import SKU
from meiduo_admin.serializers.sku import SKUModelSerializer, SKUSerializer


class SKUInfoView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = SKUModelSerializer


class SKUView(ModelViewSet):
    queryset = SKU.objects.all()