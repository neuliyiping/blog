
from django.shortcuts import render
from .models import Message,MsgNotification
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views import generic
from django.shortcuts import get_object_or_404
from . import handlers
from .models import Message
user_model = settings.AUTH_USER_MODEL

class MessageView(generic.ListView):
    model = Message
    template_name = 'message/detail.html'
    context_object_name = 'message_list'


@login_required
@require_POST
def AddMessageView(request):
    if request.is_ajax():
        data = request.POST
        new_user = request.user
        new_content = data.get('content')
        rep_id = data.get('rep_id')
        if len(new_content) > 1048:
            return JsonResponse({'msg': '你的留言字数超过1048，无法保存。'})

        if not rep_id:
            new_comment = Message(author=new_user, content=new_content,  parent=None,rep_to=None)
        else:
            new_rep_to = Message.objects.get(id=rep_id)
            new_parent = new_rep_to.parent if new_rep_to.parent else new_rep_to
            new_comment = Message(author=new_user, content=new_content, parent=new_parent,rep_to=new_rep_to)
        new_comment.save()
        new_point = '#com-' + str(new_comment.id)
        return JsonResponse({'msg': '留言提交成功！', 'new_point': new_point})
    return JsonResponse({'msg': '留言失败！'})


@login_required
def NotificationView(request, is_read=None):
    '''展示提示消息列表'''
    now_date = datetime.now()
    return render(request, 'message/notification.html', context={'is_read': is_read, 'now_date': now_date})


@login_required
@require_POST
def mark_to_read(request):
    '''将一个消息标记为已读'''
    if request.is_ajax():
        data = request.POST
        user = request.user
        id = data.get('id')
        info = get_object_or_404(MsgNotification, get_p=user, id=id)
        info.mark_to_read()
        return JsonResponse({'msg': 'mark success'})
    return JsonResponse({'msg': 'miss'})

@login_required
@require_POST
def mark_to_delete(request):
    '''将一个消息删除'''
    if request.is_ajax():
        data = request.POST
        user = request.user
        id = data.get('id')
        info = get_object_or_404(MsgNotification, get_p=user, id=id)
        info.delete()
        return JsonResponse({'msg': 'delete success'})
    return JsonResponse({'msg': 'miss'})
