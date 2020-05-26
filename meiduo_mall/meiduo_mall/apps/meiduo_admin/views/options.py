from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SpecificationOption
from meiduo_admin.serializers.options import OptionsModelSerializer
from meiduo_admin.utils.pageresponse import PageNum


class OptionsInfoView(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = SpecificationOption.objects.all()
    serializer_class = OptionsModelSerializer
    pagination_class = PageNum
