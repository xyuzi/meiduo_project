from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer
import logging

logger = logging.getLogger('django')


def generate_access_token_by_openid(openid):
    obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=600)
    dict = {
        'openid': openid
    }
    access_token = obj.dumps(dict).decode()
    return access_token


def check_access_token_by_openid(accesss_token):
    obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=600)
    try:
        openid = obj.loads(accesss_token)
    except Exception as e:
        logger.error(e)
        return None
    else:
        return openid.get('openid')
