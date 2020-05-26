from django.test import TestCase

# Create your tests here.
import os
import sys
import django

sys.path.insert(0, '../../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
django.setup()
from goods.models import GoodsChannelGroup

# group = GoodsChannelGroup.objects.all()
for i in range(1,12):
    GoodsChannelGroup.objects.create(name='频道%s'%i)
