from rest_framework import serializers

from goods.models import Brand


class BrandsInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
