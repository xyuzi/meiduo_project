from rest_framework import serializers

from goods.models import Goods, Brand, GoodsCategory


class GoodsInfoSerializers(serializers.ModelSerializer):
    brand_id = serializers.IntegerField()

    class Meta:
        model = Goods
        # brand, brand_id, category1_id, category2_id, category3_id, comments, id, name, sales
        fields = ['id', 'name', 'brand', 'brand_id', 'category1_id', 'category2_id', 'category3_id', 'sales',
                  'comments']


class GoodsBrandInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class GoodsCategoryInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']
