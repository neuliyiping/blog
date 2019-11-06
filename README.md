##### 网站拿github一哥们的  [轮子](https://github.com/Hopetree/izone "轮子")改的，代码写了详细的注释，并对一些自己不喜欢的地方做了一些修改

- 样式做了小小的改变
- 增加了留言板和照片墙
- 留言整合通知
- 去除第三方登录，准备更换qq第三方登录
- 更换后台管理
- 代码优化，更符合自己得习惯
- django1.x升级到django2.2
- 由redis缓存更换为数据库缓存
- 删除restful接口和在线工具
- 后台文章编辑增加了markdown编辑实时预览

- 文章详情页添加自己联系方式

  以上为主要修改，看源码学到了一些东西，但是基本上博客系统都是那几张表，原来想着是单纯嫖个样式，因为自己是真的没有一点设计的灵感，嫖着嫖着就将自己原来的bb代码大换血。（也发现了自己是真的菜）

##### 使用说明

- pip install -r requirements.txt

- 检查自己的配置是否为settings.local

- 迁移数据库

- python manage.py createcachetable my_cache_table(或者是你不用数据库缓存，此步忽略)

- python manage.py runserver
  
- 经过以上几步自己的博客系统就启动了

- fabfile是自动化部署用的。
##### 样式预览
以下是我的网站链接，点击进去就看到。
https://liyiping.cn/
