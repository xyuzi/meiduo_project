from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.models import OrderInfo
from meiduo_admin.serializers.orders import OrdersInfoSerializers, OrdersInforMationModelSerializer
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


class OrdersInforMationView(APIView):
    def get(self, request, pk):
        order = OrderInfo.objects.get(order_id=pk)
        serializer = OrdersInforMationModelSerializer(order)
        return Response(serializer.data)
