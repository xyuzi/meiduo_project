from rest_framework import serializers

from goods.models import Goods, Brand, GoodsCategory


class GoodsInfoSerializers(serializers.ModelSerializer):
    brand_id = serializers.IntegerField()
    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()

    class Meta:
        model = Goods
        fields = ['id', 'name', 'brand', 'brand_id', 'category1_id', 'category2_id', 'category3_id', 'sales',
                  'comments', 'desc_detail', 'desc_pack', 'desc_service']

        extra_kwargs = {
            'brand': {
                'required': False
            },
            'sales': {
                'required': False
            },
            'comments': {
                'required': False
            }
        }


class GoodsBrandInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class GoodsCategoryInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']
