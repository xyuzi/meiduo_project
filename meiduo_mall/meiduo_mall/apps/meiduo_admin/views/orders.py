from rest_framework.generics import ListAPIView

from carts.models import OrderInfo
from meiduo_admin.serializers.orders import OrdersInfoSerializers
from meiduo_admin.utils.pageresponse import PageNum


class OrdersInfoView(ListAPIView):
    serializer_class = OrdersInfoSerializers
    pagination_class = PageNum

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return OrderInfo.objects.filter(order_id=keyword)
        else:
            return OrderInfo.objects.all()
