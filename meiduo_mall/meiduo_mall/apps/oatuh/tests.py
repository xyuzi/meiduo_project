import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
from django.test import TestCase

# Create your tests here.
from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings

if __name__ == '__main__':
    # obj = TimedJSONWebSignatureSerializer(秘钥,有效期)
    obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=600)

    dict = {
        'name': '小仓唯',
        'age': 12
    }

    access_token = obj.dumps(dict).decode()

    print(access_token)

    access_token = obj.loads(access_token)
    print(access_token)
