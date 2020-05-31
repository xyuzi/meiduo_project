from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from fdfs_client.client import Fdfs_client
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import IsAdminUser

from meiduo_admin.serializers.image import SkuImageModelSerializer
from meiduo_admin.utils.pageresponse import PageNum

from goods.models import SKUImage
from meiduo_mall.utils.fastdfs.fastdfs_storage import FastDFSStorage


class SKUImageView(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = SKUImage.objects.all().order_by('sku_id')
    serializer_class = SkuImageModelSerializer
    pagination_class = PageNum

    # @method_decorator(permission_required('goods.Sku_Image', raise_exception=True))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @method_decorator(permission_required('goods.Sku_Image', raise_exception=True))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(permission_required('goods.Sku_Image', raise_exception=True))
    def create(self, request, *args, **kwargs):
        sku_id = request.data.get('sku')
        fast = FastDFSStorage()
        url = fast.save(name=None, content=request.FILES.get('image'))
        sku_img = SKUImage.objects.create(sku_id=sku_id, image=url)

        return Response(
            {
                'id': sku_img.id,
                'sku': sku_id,
                'image': sku_img.image.url
            },
            status=HTTP_201_CREATED
        )

    @method_decorator(permission_required('goods.Sku_Image', raise_exception=True))
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # fast = FastDFSStorage()
        # url = fast.save(name=None, content=request.FILES.get('image'))
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        try:
            client.delete_file(instance.image.name)
        except Exception as e:
            pass
        result = client.upload_by_buffer(request.FILES.get('image').read())
        if result.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FDFS系统失败')
        url = result.get('Remote file_id')
        instance.image = url
        instance.save()
        return Response({
            "id": instance.id,
            "sku": instance.sku_id,
            "image": instance.image.url
        },
            status=HTTP_201_CREATED
        )

    @method_decorator(permission_required('goods.Sku_Image', raise_exception=True))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        try:
            client.delete_file(instance.image.name)
        except Exception as e:
            pass
        instance.delete()
        return Response(status=HTTP_201_CREATED)
