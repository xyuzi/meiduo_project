from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED

from carts.models import OrderInfo
from meiduo_admin.serializers.orders import OrdersInfoSerializers, OrdersInforMationModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class OrdersInfoView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrdersInfoSerializers
    pagination_class = PageNum

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return OrderInfo.objects.filter(order_id=keyword)
        else:
            return OrderInfo.objects.all()

    # @method_decorator(permission_required('carts.Order_Info', raise_exception=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrdersInforMationView(APIView):
    permission_classes = [IsAdminUser]

    # @method_decorator(permission_required('carts.Order_Info', raise_exception=True))
    def get(self, request, pk):
        order = OrderInfo.objects.get(order_id=pk)
        serializer = OrdersInforMationModelSerializer(order)
        return Response(serializer.data)


class OrdersStatusView(APIView):
    permission_classes = [IsAdminUser]

    @method_decorator(permission_required('carts.Order_Info', raise_exception=True))
    def put(self, request, order_id):
        status = request.data.get('status')
        order = OrderInfo.objects.get(order_id=order_id)
        order.status = status
        order.save()
        return Response({'order_id': order_id, 'status': status}, status=HTTP_201_CREATED)
