import os
from .common import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('YiPing_SECRET_KEY', '#!kta!9e0)24d@9#=*=ra$r!0k0+p5@w+a%7g1bbof9+ad@4_(')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('YiPing_DEBUG', 'True').upper() == 'FALSE'

ALLOWED_HOSTS = ['127.0.0.1','localhost','liyiping.cn']

# SMTP服务器
EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = 'neu_liyiping@qq.com'
EMAIL_HOST_PASSWORD = '授权码'
EMAIL_PORT = 465
EMAIL_TIMEOUT = 5
# 是否使用了SSL 或者TLS，选一个为True就可以
EMAIL_USE_SSL = True
# EMAIL_USE_TLS = True
# 默认发件人，不设置的话django默认使用的webmaster@localhost
DEFAULT_FROM_EMAIL = '邮箱验证 <neu_liyiping@qq.com>'
