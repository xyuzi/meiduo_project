from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer


def generate_access_token_by_openid(openid):
    obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=600)
    dict = {'openid': openid}
    access_token = obj.dumps(dict).decode()
    return access_token
