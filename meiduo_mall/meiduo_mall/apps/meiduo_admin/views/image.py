from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.image import SkuImageModelSerializer
from meiduo_admin.utils.pageresponse import PageNum

from goods.models import SKUImage
from meiduo_mall.utils.fastdfs.fastdfs_storage import FastDFSStorage


class SKUImageView(ModelViewSet):
    queryset = SKUImage.objects.all().order_by('sku_id')
    serializer_class = SkuImageModelSerializer
    pagination_class = PageNum

    def create(self, request, *args, **kwargs):
        sku_id = request.data.get('sku')
        fast = FastDFSStorage()
        url = fast.save(name=None, content=request.FILES.get('image'))
        sku_img = SKUImage.objects.create(sku_id=sku_id, image=url)

        return Response(
            {
                'id': sku_img.id,
                'sku': sku_id,
                'image': settings.FDFS_URL+sku_img.image
            },
            status=201
        )


