from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from django.contrib.auth.models import Group, Permission

from meiduo_admin.serializers.simple import SimplenModelSerializer, GroupModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class GroupsView(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    pagination_class = PageNum


class SimplenView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = SimplenModelSerializer
