from django.db.models import Q
from django.test import TestCase

# Create your tests here.
import os
import sys
import django

sys.path.insert(0, '../../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
django.setup()
from goods.models import GoodsChannelGroup
from users.models import User
from django.contrib.auth.models import Group, Permission

# group = GoodsChannelGroup.objects.all()
# for i in range(1,12):
#     GoodsChannelGroup.objects.create(name='频道%s'%i)

# groups = Group.objects.all()
# user = User.objects.get(id=47)
# for group in groups:
#     users = group.user_set.all()
#     print(users)
# perm = Permission.objects.get(codename='view_goodschannelgroup')
# users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm) ).distinct()
# print(users)

user = User.objects.get(id=47)
print(user)
# groups = user.groups.all().distinct()
# print(groups)
permissions = user.user_permissions.all()
print(permissions)
for permission in permissions:
    print(permission.id)
