from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsChannel
from meiduo_admin.serializers.channel import ChannelInfoModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class ChannelInfoView(ModelViewSet):
    serializer_class = ChannelInfoModelSerializer
    queryset = GoodsChannel.objects.all()
    pagination_class = PageNum
