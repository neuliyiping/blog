# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from .models import Message,MsgNotification
def notify_handler(sender, instance, created, **kwargs):
    message = instance
    create_p = instance.author
    if created:
        if message.rep_to:
            if message.author == message.rep_to.author:
                get_p = message.rep_to.author
                if create_p != get_p:
                    new_notify = MsgNotification(create_p=create_p, get_p=get_p, message=message)
                    new_notify.save()

            else:
                get_p1 = message.author
                if create_p != get_p1:
                    new1 = MsgNotification(create_p=create_p, get_p=get_p1, message=message)
                    new1.save()
                get_p2 = message.rep_to.author
                if create_p != get_p2:
                    new2 = MsgNotification(create_p=create_p, get_p=get_p2, message=message)
                    new2.save()
        else:
            get_p = message.parent
            new_notify = MsgNotification(create_p=create_p, get_p_id=1, message=message)
            new_notify.save()

post_save.connect(notify_handler, sender=Message)
