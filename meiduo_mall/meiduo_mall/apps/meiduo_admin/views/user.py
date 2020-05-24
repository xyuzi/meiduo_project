from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser

from meiduo_admin.serializers.user import UserInfoModelSerializer
from meiduo_admin.utils.pageresponse import PageNum

from users.models import User


class SelectUserInfoView(ListAPIView, CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserInfoModelSerializer
    pagination_class = PageNum

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')

        if keyword:
            return User.objects.filter(username__istartswith=keyword,
                                       is_staff=False, is_superuser=False)
        else:
            return User.objects.filter(is_staff=False, is_superuser=False)
