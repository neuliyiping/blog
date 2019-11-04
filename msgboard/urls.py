# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import AddMessageView,  mark_to_read, mark_to_delete,MessageView,NotificationView

urlpatterns = [
    url(r'^add/$', AddMessageView, name='add_message'),
    url(r'^msgboard/$', MessageView.as_view(), name='message'),
    # url(r'^notification/$', NotificationView, name='msgnotification'),
    # url(r'^notification/no-read/$', NotificationView, {'is_read': 'false'}, name='msgnotification_no_read'),
    url(r'^notification/mark-to-read/$', mark_to_read, name='msg_mark_to_read'),
    url(r'^notification/mark-to-delete/$', mark_to_delete, name='msg_mark_to_delete'),
]
