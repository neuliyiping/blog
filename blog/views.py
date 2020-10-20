from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views import generic
from django.conf import settings
from .models import Article, Tag, Category, Silian, AboutBlog,Timeline,Lunch
from .utils import site_full_url
from django.core.cache import cache
from markdown.extensions.toc import TocExtension  # 锚点的拓展
import markdown
import time, datetime
from haystack.generic_views import SearchView  # 导入搜索视图
from haystack.query import SearchQuerySet


# Create your views here.

def goview(request):
    return render(request, 'test_html.html')


class ArchiveView(generic.ListView):
    """
    将归档页面返回，/archive/
    """
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'articles'
    paginate_by = 200
    paginate_orphans = 50


class IndexView(generic.ListView):
    model = Article
    template_name = 'blog/index.html'#返回的渲染的模板
    context_object_name = 'articles'#给 get_queryset 方法返回的 model 列表重新命名，不指定的话是object_list
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        """
        重写父类方法。父类返回的是None，在get_queryset方法中会用到，父类用ordering如下
        queryset = queryset.order_by(*ordering)
        :return:
        """
        sort = self.kwargs.get('sort')
        #判断排序方法，其中时间排序没有传入任何值，而热度排序传入了一个字典，url(r'^hot/$', IndexView.as_view(), {'sort': 'v'}, name='index_hot')
        if sort == 'v':#热度排序
            return ('-views', '-update_date', '-id')
        return ('-is_top', '-create_date')


class DetailView(generic.DetailView):
    """
    将文章详情页返回
    """
    model = Article#获取模型
    template_name = 'blog/detail.html'#返回的模板名称
    context_object_name = 'article'#模板渲染数据名称

    def get_object(self,queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 article 的 body 值进行渲染
        obj = super(DetailView, self).get_object()
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过半小时才重新统计阅览量,作者浏览忽略
        u = self.request.user#获取访问者username,未登录用户是AnonymousUser
        ses = self.request.session#获取访问者的session
        the_key = 'is_read_{}'.format(obj.id)
        #sessions:dict_keys(['is_read_2', '_auth_user_id', '_auth_user_backend', '_auth_user_hash', '_session_expiry'])
        is_read_time = ses.get(the_key)
        if u != obj.author:
            if not is_read_time:#session中没有此值，说明是未登录用户
                obj.update_views()
                ses[the_key] = time.time()
            else:
                #如果是登录用户则30分钟增加一次浏览记录
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 30:
                    obj.update_views()
                    ses[the_key] = time.time()
        # 获取文章更新的时间，判断是否从缓存中取文章的markdown,可以避免每次都转换
        ud = obj.update_date.strftime("%Y%m%d%H%M%S")
        md_key = '{}_md_{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            md = cache_md
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',#代码高亮

                # 记得在顶部引入 TocExtension 和 slugify
                # TocExtension 在实例化时其 slugify 参数可以接受一个函数，这个函数将被用于处理标题的锚点值。Markdown
                # 内置的处理方法不能处理中文标题，所以我们使用了django.utils.text中的slugify方法，该方法可以很好地处理中文。
                #
                # 什么是锚点值：http://127.0.0.1:8000/posts/8/#_3     #_3就是锚点

                TocExtension(slugify=slugify)
            ])
            cache.set(md_key, md, 60 * 60 * 12)
        obj.body = md.convert(obj.body)#将markdown文档转换为html
        obj.toc = md.toc#markdown自动生成的目录
        return obj


class CategoryView(generic.ListView):
    model = Article#指定获取模型
    template_name = 'blog/category.html'#返回模板名称
    context_object_name = 'articles'#渲染模板数据名称
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        """
        重写父类get_ordering方法，
        :return:
        """
        ordering = super(CategoryView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs):
        """
            该方法默认获取指定模型的全部列表数据。
            为了获取指定分类下的文章列表数据，我们覆写该方法，改变它的默认行为。
            """
        queryset = super(CategoryView, self).get_queryset()

        # url视图中的url(r'^category/(?P<slug>[\w-]+)/$'）slug是命名组
        # 在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，
        # 非命名组参数值保存在实例的 args 属性（是一个列表）里。
        # 所以我们使了 self.kwargs.get('slug') 来获取从 URL 捕获的分类 slug 值。
        # 然后我们调用父类的 get_queryset 方法获得全部文章列表，
        # 紧接着就对返回的结果调用了 filter 方法来筛选该分类下的全部文章并返回。

        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=cate)

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 articles 传递给模板外（DetailView 已经帮我们完成），
        #将文章分类传递给模板
        context_data = super(CategoryView, self).get_context_data()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章分类'
        context_data['search_instance'] = cate
        return context_data


class TagView(generic.ListView):
    model = Article#指定模型名称
    template_name = 'blog/tag.html'#指定模板名称
    context_object_name = 'articles'#渲染模板数据名称
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        """
        重写父类排序方法。
        :return:
        """
        ordering = super(TagView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs):
        """
        返回tag下的时间排序或热度排序
        :param kwargs:
        :return:
        """
        queryset = super(TagView, self).get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=tag)

    def get_context_data(self, **kwargs):
        """
        将关于tag分类,加入到返回的模板数据中
        :param kwargs:
        :return:
        """
        context_data = super(TagView, self).get_context_data()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章标签'
        context_data['search_instance'] = tag
        return context_data

def AboutView(request):
    obj = AboutBlog.objects.first()
    if obj:
        ud = obj.update_date.strftime("%Y%m%d%H%M%S")
        md_key = '{}_md_{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            body = cache_md
        else:
            body = obj.body_to_markdown()
            cache.set(md_key, body, 3600 * 24 * 15)
    else:
        repo_url = 'https://github.com/neuliyiping'
        body = '<li>作者 Github 地址：<a href="{}">{}</a></li>'.format(repo_url, repo_url)
    return render(request, 'blog/about.html', context={'body': body})

def LunchView(request):
    data = Lunch.objects.values_list()
    lunches = []
    for item in data:
        lunches.append(item[1])
    return render(request, 'blog/lunch.html', context={'data': ' '.join(lunches)})

class TimelineView(generic.ListView):
    model = Timeline
    template_name = 'blog/timeline.html'
    context_object_name = 'timeline_list'


class SilianView(generic.ListView):
    model = Silian
    template_name = 'blog/silian.xml'
    context_object_name = 'badurls'


# 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
class MySearchView(SearchView):
    context_object_name = 'search_list'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    queryset = SearchQuerySet().order_by('-views')


def robots(request):
    site_url = site_full_url()
    return render(request, 'robots.txt', context={'site_url': site_url}, content_type='text/plain')


class MsgBoardView(generic.ListView):
    pass

class PhotoWallView(generic.ListView):
    pass