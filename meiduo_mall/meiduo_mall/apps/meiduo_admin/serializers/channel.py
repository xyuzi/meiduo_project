from rest_framework import serializers

from goods.models import GoodsChannel


class ChannelInfoModelSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField()
    group_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    category = serializers.StringRelatedField()


    class Meta:
        model = GoodsChannel
        fields = ['category', 'category_id', 'group_id', 'group', 'id', 'sequence', 'url']
