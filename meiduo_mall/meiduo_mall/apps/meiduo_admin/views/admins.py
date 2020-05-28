from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from meiduo_admin.serializers.admins import AdminsModelSerializer, AdminSimplenModelSerializer
from meiduo_admin.utils.pageresponse import PageNum
from users.models import User


class AdminsView(ModelViewSet):
    # or 查询
    # queryset = User.objects.filter(Q(is_superuser=True) | Q(is_staff=True))
    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminsModelSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]

    # 模型类以实现 ↓list↓可以达到相同要求
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     group_list = []
    #     permission_list = []
    #     for user in queryset:
    #         for group in user.groups.all():
    #             group_list.append(group.id)
    #         for permission in user.user_permissions.all():
    #             permission_list.append(permission.id)
    #
    #     serializer = self.get_serializer(page, many=True)
    #     serializer.data.groups = group_list
    #     serializer.data.user_permissions = permission_list
    #     return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        instance = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        groups = instance.pop('groups')
        permissions = instance.pop('user_permissions')
        user = User.objects.create_user(username=instance.get('username', 'username'),
                                        email=instance.get('email', ''),
                                        mobile=instance.get('mobile', ''),
                                        password=instance.get('password'),
                                        is_staff=True)
        group_list = []
        permission_list = []
        for group in groups:
            user.groups.add(group)
            group_list.append(group)
        for permission in permissions:
            user.user_permissions.add(permission)
            permission_list.append(permission)

        return Response({
            "id": user.id,
            "username": user.username,
            "password": '',
            "mobile": user.mobile,
            "email": user.email,
            "groups": group_list,
            "user_permissions": permission_list
        })

    # 模型类以实现 ↓update↓可以达到相同要求
    # def update(self, request, *args, **kwargs):
    #     instance = request.data
    #     user = self.get_object()
    #     serializer = self.get_serializer(user, request.data)
    #     serializer.is_valid(raise_exception=True)
    #     groups = instance.pop('groups')
    #     permissions = instance.pop('user_permissions')
    #     user.username = instance.get('username', 'username')
    #     user.email = instance.get('email', '')
    #     user.mobile = instance.get('mobile', '')
    #
    #     group_list = []
    #     permission_list = []
    #     for group in groups:
    #         user.groups.add(group)
    #         group_list.append(group)
    #     for permission in permissions:
    #         user.user_permissions.add(permission)
    #         permission_list.append(permission)
    #
    #     return Response({
    #         "id": user.id,
    #         "username": user.username,
    #         "mobile": user.mobile,
    #         "email": user.email,
    #         "groups": group_list,
    #         "user_permissions": permission_list
    #     })


class AdminSimplenView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = AdminSimplenModelSerializer
