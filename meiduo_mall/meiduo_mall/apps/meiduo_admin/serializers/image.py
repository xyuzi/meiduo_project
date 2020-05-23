from rest_framework import serializers

from goods.models import SKUImage


class SkuImageModelSerializer(serializers.ModelSerializer):
    sku = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SKUImage
        fields = ['id', 'sku', 'image']
