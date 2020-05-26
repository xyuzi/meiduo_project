from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from goods.models import GoodsChannel, GoodsCategory, GoodsChannelGroup
from meiduo_admin.serializers.channel import ChannelInfoModelSerializer, ChannelGroupModelSerializer, \
    ChannelCategoriesModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class ChannelInfoView(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = ChannelInfoModelSerializer
    queryset = GoodsChannel.objects.all().order_by('group_id', 'sequence')
    pagination_class = PageNum


class ChannelCategoriesView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = GoodsCategory.objects.all()
    serializer_class = ChannelCategoriesModelSerializer


class ChannelGroupView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = GoodsChannelGroup.objects.all()
    serializer_class = ChannelGroupModelSerializer
