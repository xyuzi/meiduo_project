from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from django.contrib.auth.models import Group, Permission

from meiduo_admin.serializers.simple import SimplenModelSerializer, GroupModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class GroupsView(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    pagination_class = PageNum

    # @method_decorator(permission_required('auth.Group_group', raise_exception=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @method_decorator(permission_required('auth.Group_group', raise_exception=True))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(permission_required('auth.Group_group', raise_exception=True))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(permission_required('auth.Group_group', raise_exception=True))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(permission_required('auth.Group_group', raise_exception=True))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class SimplenView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = SimplenModelSerializer

    # @method_decorator(permission_required('auth.Permission_permission', raise_exception=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
