import os
from .common import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('YiPing_SECRET_KEY', '#!kta!9e0)24d@9#=*=ra$r!0k0+p5@w+a%7g1bbof9+ad@4_(')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('YiPing_DEBUG', 'True').upper() == 'TRUE'

ALLOWED_HOSTS = ['127.0.0.1','localhost','liyiping.cn']