from rest_framework import serializers

from carts.models import OrderInfo


class OrdersInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ['order_id', 'create_time']
