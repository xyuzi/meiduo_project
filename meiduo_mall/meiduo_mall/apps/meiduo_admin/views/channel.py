from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
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

    # @method_decorator(permission_required('goods.Goods_Channel'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @method_decorator(permission_required('goods.Goods_Channel'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Channel'))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Channel'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Goods_Channel'))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ChannelCategoriesView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = GoodsCategory.objects.all()
    serializer_class = ChannelCategoriesModelSerializer

    # @method_decorator(permission_required('goods.Goods_Category'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ChannelGroupView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = GoodsChannelGroup.objects.all()
    serializer_class = ChannelGroupModelSerializer

    # @method_decorator(permission_required('goods.Goods_Channel'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
