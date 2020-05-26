from rest_framework import serializers

from goods.models import SKU, GoodsCategory, Goods, GoodsSpecification, SpecificationOption, SKUSpecification

from django.db import transaction


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
    spu_id = serializers.IntegerField(label='商品id', )
    category_id = serializers.IntegerField(label='从属类别id', )
    spu = serializers.StringRelatedField(required=False)
    category = serializers.StringRelatedField(required=False)
    specs = SpecsSerializer(many=True)

    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        specs = validated_data.pop('specs')
        with transaction.atomic():
            save_point = transaction.savepoint()
            sku = SKU.objects.create(**validated_data)
            for spec in specs:
                SKUSpecification.objects.create(sku=sku, **spec)

            transaction.savepoint_commit(save_point)
            return sku

    def update(self, instance, validated_data):
        specs = validated_data.pop('specs')
        with transaction.atomic():
            save_point = transaction.savepoint()
            instance = super().update(instance, validated_data)
            for spec in specs:
                SKUSpecification.objects.filter(sku=instance, spec_id=spec.get('spec_id')).update(
                    option_id=spec.get('option_id'))

            transaction.savepoint_commit(save_point)
            return instance


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
