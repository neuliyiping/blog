
from django.db import models
from imagekit.models import ProcessedImageField
#不能装imagekit的库，而要装django-imagekit
from imagekit.processors import ResizeToFill

class Photos(models.Model):
    title=models.CharField(verbose_name='标题',max_length=128,default='简述')
    desc = models.CharField(max_length=256,verbose_name='图片描述')
    # image = ProcessedImageField(upload_to='images/%Y/%m/%d',
    #                              verbose_name='图片',
    #                              )
    image = models.CharField(verbose_name='图床链接',max_length=256)
    isshow=models.BooleanField(default=True,verbose_name='是否展示')
    class Meta:
        verbose_name = '照片墙'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return str(self.desc)
