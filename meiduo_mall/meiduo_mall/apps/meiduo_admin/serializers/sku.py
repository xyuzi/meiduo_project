from rest_framework import serializers

from goods.models import SKU, GoodsCategory, Goods, GoodsSpecification, SpecificationOption


class SKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['id', 'name']


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'


class SKUThreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['id', 'name']


class SpecificationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = ['id', 'value']


class GoodsSpecificationSerializer(serializers.ModelSerializer):
    options = SpecificationOptionSerializer(many=True)

    class Meta:
        model = GoodsSpecification
        fields = ['id', 'name', 'spu', 'options']
