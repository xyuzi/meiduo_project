from rest_framework import serializers

from goods.models import GoodsChannel, GoodsCategory, GoodsChannelGroup


class ChannelInfoModelSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    group_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    category = serializers.StringRelatedField()

    class Meta:
        model = GoodsChannel
        fields = ['category', 'category_id', 'group_id', 'group', 'id', 'sequence', 'url']


class ChannelGroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsChannelGroup
        fields = ['id', 'name']


class ChannelCategoriesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']
