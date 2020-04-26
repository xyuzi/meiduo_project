from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings
import logging

logger = logging.getLogger('django')


# Create your models here.
class User(AbstractUser):
    """自定义用户模型类"""

    # 额外增加 mobile 字段
    mobile = models.CharField(max_length=11,
                              unique=True,
                              verbose_name='手机号')
    email_active = models.BooleanField(default=False,
                                       verbose_name='邮箱验证')

    # 对当前表进行相关设置:
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_verify_email_url(self):
        '''加密'''
        obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=60 * 60 * 24)
        dict = {
            'user_id': self.id,
            'email': self.email
        }
        token = obj.dumps(dict).decode()
        url = settings.EMAIL_VERIFY_URL + token
        return url

    @staticmethod
    def check_verify_email_token(token):
        '''解码'''
        obj = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=60 * 60 * 24)
        try:
            data = obj.loads(token)
        except Exception as e:
            logger.error(e)
            return None
        else:
            user_id = data.get('user_id')
            email = data.get('email')

        try:
            user = User.objects.get(id=user_id, email=email)
        except Exception as e:
            logger.error(e)
            return None
        else:
            return user
