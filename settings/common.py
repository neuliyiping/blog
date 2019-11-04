
import os
import sys

# 更换默认的数据库连接
import pymysql

pymysql.install_as_MySQLdb()
# 导入网站个人信息，非通用信息

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 添加 apps 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

INSTALLED_APPS = [
    'simpleui',
    'crispy_forms',  # bootstrap表单样式
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',  # 网站地图
    'oauth.apps.OauthConfig',
    'msgboard.apps.MsgboardConfig',
    # allauth需要注册的应用
    'django.contrib.sites',  # 这个是自带的，会创建一个sites表，用来存放域名
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "mdeditor",# md文档后台实时预览
    'haystack',
    'blog.apps.App01Config',
    'comment.apps.CommentConfig',
    'photowall.apps.PhotowallConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


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
                'blog.context_processors.settings_info',  # 自定义上下文管理器
            ],
        },
    },
]

WSGI_APPLICATION = 'myblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, "static")



# 配置用户上传的文件
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 需要配置TEMPLATES


# UserProfile 覆盖了 django 内置的 users 表
AUTH_USER_MODEL = 'oauth.Ouser'

# 网站默认设置和上下文信息
SITE_END_TITLE = os.getenv('YiPing_SITE_END_TITLE', '')
SITE_DESCRIPTION = os.getenv('YiPing_SITE_DESCRIPTION', '追求源于热爱')
SITE_KEYWORDS = os.getenv('YiPing_SITE_KEYWORDS', '李一平,Django博客,个人博客')
#分页用
BASE_PAGE_BY = 10
BASE_ORPHANS = 5

# allauth配置
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
LOGIN_REDIRECT_URL = "/"#注冊登錄跳轉頁面

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# allauth需要的配置
# 当出现"SocialApp matching query does not exist"这种报错的时候就需要更换这个ID
SITE_ID = 1

ROOT_URLCONF = 'myblog.urls'
# Email setting
# 注册中邮件验证方法:“强制（mandatory）”,“可选（optional）【默认】”或“否（none）”之一。
# 开启邮箱验证的话，如果邮箱配置不可用会报错，所以默认关闭，根据需要自行开启
ACCOUNT_EMAIL_VERIFICATION = os.getenv('YiPing_ACCOUNT_EMAIL_VERIFICATION', 'none')
# 登录方式，选择用户名或者邮箱都能登录
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# 设置用户注册的时候必须填写邮箱地址
ACCOUNT_EMAIL_REQUIRED = True
# 登出直接退出，不用确认
ACCOUNT_LOGOUT_ON_GET = True

# 表单插件的配置
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# restframework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

# 个性化设置，非必要信息
# 个人 Github 地址
MY_GITHUB = os.getenv('YiPing_GITHUB', 'https://github.com/neuliyiping')
# 工信部备案信息
BEIAN = os.getenv('YiPing_BEIAN', '网站备案信息')
# 站长统计（友盟）
CNZZ_PROTOCOL = os.getenv('YiPing_CNZZ_PROTOCOL', '')
# 站长推送
MY_SITE_VERIFICATION = os.getenv('YiPing_SITE_VERIFICATION', '')
# 使用 http 还是 https （sitemap 中的链接可以体现出来）
PROTOCOL_HTTPS = os.getenv('YiPing_PROTOCOL_HTTPS', 'HTTP').lower()
#缓存设置

# CACHES={
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', #缓存到本地内存中
#         'TIMEOUT': 60,
#     }
# }
#文件缓存
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#        'LOCATION': '/django_cache',
#          'TIMEOUT': 600,
#           'OPTIONS': {
#                'MAX_ENTRIES': 1000
#        }
#    }
#}
# 数据库缓存
CACHES = {
     'default': {
         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
         'LOCATION': 'my_cache_table', # 设置一个数据库存放缓存的表名
     }
     #其他的配置和开发调试版本一样
 }
