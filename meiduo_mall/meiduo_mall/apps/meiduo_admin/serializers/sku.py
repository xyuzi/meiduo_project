from rest_framework import serializers

from goods.models import SKU


class SKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['id', 'name']
