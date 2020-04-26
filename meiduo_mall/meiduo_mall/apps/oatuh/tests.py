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
    # access_token = obj.loads('eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4Nzg2NzIxNCwiZXhwIjoxNTg3ODY3ODE0fQ.eyJuYW1lIjoi5bCP5LuT5ZSvIiwiYWdlIjoxMn0.J8c93RtZrISXQM1_0D6uFzvPNa7IrW0w9hgwD50ceRSn3zLJzz9Z41Mh7H1284n585jrqeVviu6veyYQP_94L1')
    print(access_token.get('name'))
