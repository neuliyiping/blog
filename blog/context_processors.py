# -*- coding: utf-8 -*-

from django.conf import settings

# 自定义上下文管理器
def settings_info(request):
    return {
        'site_end_title':settings.SITE_END_TITLE,
        'site_description':settings.SITE_DESCRIPTION,
        'site_keywords':settings.SITE_KEYWORDS,
        'cnzz_protocol':settings.CNZZ_PROTOCOL,
        'beian':settings.BEIAN,
        'my_github':settings.MY_GITHUB,
        'site_verification':settings.MY_SITE_VERIFICATION,
    }