from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from meiduo_admin.serializers.admins import AdminsModelSerializer, AdminSimplenModelSerializer
from meiduo_admin.utils.pageresponse import PageNum
from users.models import User


class AdminsView(ModelViewSet):
    queryset = User.objects.filter(Q(is_superuser=True) | Q(is_staff=True))
    serializer_class = AdminsModelSerializer
    pagination_class = PageNum


class AdminSimplenView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = AdminSimplenModelSerializer
