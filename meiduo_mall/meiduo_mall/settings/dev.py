"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加'apps'到路由列表
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '81o4a5e9m6h)q1^_c_%=^$il@$z*@=ml(54mt1f$po&oy!-x!f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['api.meiduo.site',
                 '127.0.0.1',
                 'localhost',
                 'www.meiduo.site']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'users',
    'verifications',
    'oatuh',
    'areas',
    'contents',
    'goods',
    'django_crontab',
    'haystack',
    'carts',
    'orders',
    'payment',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'mysql',
        'NAME': 'meiduo_mall'
    }
}

# DATABASES = {
#     'default': {  # 写（主机）
#         'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
#         'HOST': '127.0.0.1',  # 数据库主机
#         'PORT': 3306,  # 数据库端口
#         'USER': 'root',  # 数据库用户名
#         'PASSWORD': 'mysql',  # 数据库用户密码
#         'NAME': 'meiduo_mall'  # 数据库名字
#     },
#     'slave': {  # 读（从机）
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': '127.0.0.1',
#         'PORT': 8306,
#         'USER': 'root',
#         'PASSWORD': '123456',
#         'NAME': 'meiduo_mall'
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

CACHES = {
    "default": {  # 默认存储信息: 存到 0 号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session 信息: 存到 1 号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": {  # 验证码 信息: 存到 2 号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 历史记录 信息: 存到 4 号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "carts": {  # 购物车 信息: 存到 5 号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

AUTH_USER_MODEL = 'users.User'

# CORS跨域请求白名单设置
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://www.meiduo.site:8080',
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# 指定自定义的用户认证后端:
AUTHENTICATION_BACKENDS = ['users.utils.UsernameMobileAuthBackend']

# QQ登录参数
# 申请的 客户端id
QQ_CLIENT_ID = ''
# 申请的 客户端秘钥
QQ_CLIENT_SECRET = ''
# 申请时添加的: 登录成功后回调的路径
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

# 发送短信的相关设置, 这些设置是当用户没有发送相关字段时, 默认使用的内容:
# 发送短信必须进行的设置:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 使用的 smtp服务器 地址
EMAIL_HOST = 'smtp.163.com'
# 端口号
EMAIL_PORT = 25
# 下面的内容是可变的, 随后台设置的不同而改变:
# 发送邮件的邮箱
EMAIL_HOST_USER = ''
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = ''
# 收件人看到的发件人
EMAIL_FROM = ''
# 激活邮件拼接地址
EMAIL_VERIFY_URL = 'http://www.meiduo.site:8080/success_verify_email.html?token='

# FDFS需要的配置文件路径(即: client.conf文件绝对路径).
FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')
# FDFS中storage和tracker位置.端口规定死是8888, ip换成自己的ip
FDFS_URL = 'http://192.168.180.130:8888/'

DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.fastdfs_storage.FastDFSStorage'

GENERATED_STATIC_HTML_FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'front_end_pc')

# 定时任务
CRONJOBS = [
    # 每1分钟生成一次首页静态文件
    ('*/1 * * * *', 'contents.generate_index.generate_static_index_html',
     '>> ' + os.path.join(os.path.dirname(BASE_DIR), 'logs/crontab.log'))
]
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.180.130:9200/',  # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'meiduo_mall',  # Elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 4


# 支付宝相关设置
ALIPAY_APPID = '2016102200739447'
ALIPAY_DEBUG = True
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
ALIPAY_RETURN_URL = "http://www.meiduo.site:8080/pay_success.html"

# 数据库主从规则
# DATABASE_ROUTERS = ['meiduo_mall.utils.db_router.MasterSlaveDBRouter']
