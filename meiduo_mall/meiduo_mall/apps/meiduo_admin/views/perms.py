from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission, ContentType
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from meiduo_admin.serializers.perms import PermissionModelSerializer, PermissionGroupModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class PermissionView(ModelViewSet):
    serializer_class = PermissionModelSerializer
    queryset = Permission.objects.all()
    pagination_class = PageNum

    @method_decorator(permission_required('auth.Permission_permission'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(permission_required('auth.Permission_permission'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(permission_required('auth.Permission_permission'))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(permission_required('auth.Permission_permission'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(permission_required('auth.Permission_permission'))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PermissionGroupView(ListAPIView):
    serializer_class = PermissionGroupModelSerializer
    queryset = ContentType.objects.all()

    @method_decorator(permission_required('contenttypes.Content_Type'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)