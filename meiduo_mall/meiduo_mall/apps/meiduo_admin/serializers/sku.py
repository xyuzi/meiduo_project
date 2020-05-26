from rest_framework import serializers

from goods.models import SKU, GoodsCategory, Goods, GoodsSpecification, SpecificationOption, SKUSpecification


class SKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['id', 'name']


class SpecsSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ['spec_id', 'option_id']


class SKUSerializer(serializers.ModelSerializer):
    spu_id = serializers.IntegerField(label='商品id', write_only=True)
    category_id = serializers.IntegerField(label='从属类别id', write_only=True)
    spu = serializers.StringRelatedField(required=False)
    category = serializers.StringRelatedField(required=False)
    specs = SpecsSerializer(many=True)

    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        specs = validated_data.pop('specs')
        sku = SKU.objects.create(**validated_data)
        for spec in specs:
            SKUSpecification.objects.create(sku=sku, **spec)
        return sku


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
