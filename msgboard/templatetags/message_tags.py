# 创建了新的tags标签文件后必须重启服务器

from django import template
from ..models import emoji_info
from ..models import Message,MsgNotification
register = template.Library()



@register.simple_tag
def get_parent_messages():
    lis = Message.objects.filter(parent=None).order_by("-id")[:20]
    return lis


@register.simple_tag
def get_child_messages(com):
    lis = com.child_messages.all()
    return lis



@register.simple_tag
def get_notifications_messages_count(user, f=None):
    '''获取一个用户的对应条件下的提示信息'''
    if f == 'true':
        lis = user.msgnotification_get.filter(is_read=True)
    elif f == 'false':
        lis = user.msgnotification_get.filter(is_read=False)
    else:
        lis = user.msgnotification_get.all()
    return lis


@register.simple_tag
def get_notifications_messages(user,f=None):
    '''获取一个用户的对应条件下的提示信息总数'''
    if f == 'true':
        lis = user.msgnotification_get.filter(is_read=True)
    elif f == 'false':
        lis = user.msgnotification_get.filter(is_read=False)
    else:
        lis = user.msgnotification_get.all()
    return lis.count()


@register.simple_tag
def get_emoji_imgs():
    '''
    返回一个列表，包含表情信息
    :return:
    '''
    return emoji_info


@register.filter(is_safe=True)
def emoji_to_url(value):
    """
    将emoji表情的名称转换成图片地址
    """
    emoji_static_url = 'comment/qq/{}.png'
    return emoji_static_url.format(value)
