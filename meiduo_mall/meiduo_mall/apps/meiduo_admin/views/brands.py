from fdfs_client.client import Fdfs_client
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from goods.models import Brand
from meiduo_admin.serializers.brands import BrandsInfoModelSerializer
from meiduo_admin.utils.pageresponse import PageNum
from meiduo_mall.utils.fastdfs.fastdfs_storage import FastDFSStorage


class BrandsInfoView(ModelViewSet):
    serializer_class = BrandsInfoModelSerializer
    queryset = Brand.objects.all()
    pagination_class = PageNum

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        first_letter = request.data.get('first_letter')
        fast = FastDFSStorage()
        url = fast.save(name=None, content=request.FILES.get('logo'))
        brand = Brand.objects.create(name=name, logo=url, first_letter=first_letter)

        return Response(
            {
                "id": brand.id,
                "name": brand.name,
                "logo": brand.logo.url,
                "first_letter": brand.first_letter
            },
            status=HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        try:
            client.delete_file(instance.logo.name)
        except Exception as e:
            pass
        result = client.upload_by_buffer(request.FILES.get('logo').read())
        if result.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FDFS系统失败')
        url = result.get('Remote file_id')
        instance.logo = url
        instance.name = request.data.get('name')
        instance.first_letter = request.data.get('first_letter')
        instance.save()
        return Response({
            "id": instance.id,
            "name": instance.name,
            "logo": instance.logo.url,
            "first_letter": instance.first_letter
        },
            status=HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        try:
            client.delete_file(instance.logo.name)
        except Exception as e:
            pass
        instance.delete()
        return Response(status=HTTP_201_CREATED)
