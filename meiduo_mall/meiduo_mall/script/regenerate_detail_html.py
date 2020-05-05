#!/home/ubuntu/.virtualenvs/meiduo_env/bin/python
import sys

sys.path.insert(0, '../../')
from celery_tasks.html.tasks import generate_static_sku_detail_html
from goods.models import SKU

skus = SKU.objects.all()
for sku in skus:
    generate_static_sku_detail_html.delay(sku.id)
