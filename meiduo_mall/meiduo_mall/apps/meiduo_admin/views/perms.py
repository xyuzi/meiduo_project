from django.contrib.auth.models import Permission, ContentType
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from meiduo_admin.serializers.perms import PermissionModelSerializer, PermissionGroupModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class PermissionView(ModelViewSet):
    serializer_class = PermissionModelSerializer
    queryset = Permission.objects.all()
    pagination_class = PageNum


class PermissionGroupView(ListAPIView):
    serializer_class = PermissionGroupModelSerializer
    queryset = ContentType.objects.all()
