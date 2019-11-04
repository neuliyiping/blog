"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import django
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import ArticleSitemap, CategorySitemap, TagSitemap
from blog.feeds import AllArticleRssFeed
from blog.views import robots
from django.views.static import serve
from django.urls import path
# 网站地图
sitemaps = {
    'articles': ArticleSitemap,
    'tags': TagSitemap,
    'categories': CategorySitemap
}
urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/blog/img/favicon.ico')),
    url(r'^adminx/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),  # allauth
    url(r'^accounts/', include(('oauth.urls','oauth'),namespace='oauth')),  # oauth,只展现一个用户登录界面
    url('', include(('blog.urls','blog'),namespace='blog')),  # blog
    url(r'^comment/',include(('comment.urls','comment'),namespace='comment')), # comment
    url(r'^robots\.txt$', robots, name='robots'), # robots
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'), # 网站地图
    url(r'^feed/$', AllArticleRssFeed(), name='rss'),   # rss订阅
    url(r'mdeditor/', include('mdeditor.urls')),
    url('',include(('photowall.urls','photowall'),namespace='photowall')),  # 照片墙
    url('', include(('msgboard.urls','msgboard'), namespace='msgboard')),  # 留言板
    url(r'^media/(?P<path>.*)', serve, {"document_root":settings.MEDIA_ROOT}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件
