from django.db import models
from django.conf import settings
import re
import markdown

emoji_info = [
    [('aini_org', '爱你'), ('baibai_thumb', '拜拜'),
     ('baobao_thumb', '抱抱'), ('beishang_org', '悲伤'),
     ('bingbujiandan_thumb', '并不简单'), ('bishi_org', '鄙视'),
     ('bizui_org', '闭嘴'), ('chanzui_org', '馋嘴')],
    [('chigua_thumb', '吃瓜'), ('chongjing_org', '憧憬'),
     ('dahaqian_org', '哈欠'), ('dalian_org', '打脸'),
     ('ding_org', '顶'), ('doge02_org', 'doge'),
     ('erha_org', '二哈'), ('gui_org', '跪了')],
    [('guzhang_thumb', '鼓掌'), ('haha_thumb', '哈哈'),
     ('heng_thumb', '哼'), ('huaixiao_org', '坏笑'),
     ('huaxin_org', '色'), ('jiyan_org', '挤眼'),
     ('kelian_org', '可怜'), ('kuxiao_org', '允悲')],
    [('ku_org', '酷'), ('leimu_org', '泪'),
     ('miaomiao_thumb', '喵喵'), ('ningwen_org', '疑问'),
     ('nu_thumb', '怒'), ('qian_thumb', '钱'),
     ('sikao_org', '思考'), ('taikaixin_org', '太开心')],
    [('tanshou_org', '摊手'), ('tianping_thumb', '舔屏'),
     ('touxiao_org', '偷笑'), ('tu_org', '吐'),
     ('wabi_thumb', '挖鼻'), ('weiqu_thumb', '委屈'),
     ('wenhao_thumb', '费解'), ('wosuanle_thumb', '酸')],
    [('wu_thumb', '污'), ('xiaoerbuyu_org', '笑而不语'),
     ('xiaoku_thumb', '笑cry'), ('xixi_thumb', '嘻嘻'),
     ('yinxian_org', '阴险'), ('yun_thumb', '晕'),
     ('zhouma_thumb', '怒骂'), ('zhuakuang_org', '抓狂')]
]


def get_emoji_imgs(body):
    '''
    替换掉评论中的标题表情，并且把表情替换成图片地址
    :param body:
    :return:
    '''
    img_url = '<img class="comment-emoji-img" src="/static/message/weibo/{}.png" title="{}" alt="{}">'
    for i in emoji_info:
        for ii in i:
            emoji_url = img_url.format(ii[0], ii[1], ii[0])
            body = re.sub(':{}:'.format(ii[0]), emoji_url, body)
    tag_info = {
        '<h\d>': '',
        '</h\d>': '<br>'
    }
    for k, v in tag_info.items():
        body = re.sub(k, v, body)
    return body


class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_related', verbose_name='留言人',on_delete=models.CASCADE)
    create_date = models.DateTimeField('留言时间', auto_now_add=True)
    content = models.TextField('留言内容')
    parent = models.ForeignKey('self', verbose_name='父留言', related_name='child_messages', blank=True,null=True,on_delete=models.CASCADE)
    rep_to = models.ForeignKey('self', verbose_name='回复', related_name='rep_messages', blank=True, null=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']


    def __str__(self):
        return self.content[:20]

    def content_to_markdown(self):
        to_md = markdown.markdown(self.content,
                                  safe_mode='escape',
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                  ])
        return get_emoji_imgs(to_md)



class MsgNotification(models.Model):
    create_p = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='提示创建者', related_name='msgnotification_create',on_delete=models.CASCADE)
    get_p = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='提示接收者', related_name='msgnotification_get',on_delete=models.CASCADE)
    message = models.ForeignKey(Message, verbose_name='所属留言', related_name='the_message',on_delete=models.CASCADE)
    create_date = models.DateTimeField('提示时间', auto_now_add=True)
    is_read = models.BooleanField('是否已读', default=False)
    def mark_to_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])

    class Meta:
        verbose_name = '提示信息'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return '{}回复了你的留言'.format(self.create_p)
