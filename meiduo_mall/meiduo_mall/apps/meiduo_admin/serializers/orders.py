from rest_framework import serializers

from carts.models import OrderInfo, OrderGoods
from goods.models import SKU


class OrdersInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ['order_id', 'create_time']


class SKUImageInfo(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, read_only=True)
    default_image_url = serializers.CharField(max_length=200, read_only=True)

    class Meta:
        model = SKU
        fields = ['name', 'default_image_url']


class SKUInfo(serializers.ModelSerializer):
    sku = SKUImageInfo()

    class Meta:
        model = OrderGoods
        fields = ['count', 'price', 'sku']


class OrdersInforMationModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    skus = SKUInfo(many=True)

    class Meta:
        model = OrderInfo
        fields = ['order_id', 'user', 'total_count', 'total_amount', 'freight', 'pay_method', 'status', 'create_time',
                  'skus']
        # exclude = ['id','update_time']
