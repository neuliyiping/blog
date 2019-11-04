# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import imageListView

urlpatterns = [
    # url(r'^go/$', goview, name='go'),  # 测试用页面
    url(r'^photowall$', imageListView, name='photowall'),  # 主页，自然排序

]
