# Generated by Django 2.2.5 on 2020-10-16 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('msgboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='msgnotification',
            name='create_p',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msgnotification_create', to=settings.AUTH_USER_MODEL, verbose_name='提示创建者'),
        ),
        migrations.AddField(
            model_name='msgnotification',
            name='get_p',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msgnotification_get', to=settings.AUTH_USER_MODEL, verbose_name='提示接收者'),
        ),
        migrations.AddField(
            model_name='msgnotification',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_message', to='msgboard.Message', verbose_name='所属留言'),
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_related', to=settings.AUTH_USER_MODEL, verbose_name='留言人'),
        ),
        migrations.AddField(
            model_name='message',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_messages', to='msgboard.Message', verbose_name='父留言'),
        ),
        migrations.AddField(
            model_name='message',
            name='rep_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rep_messages', to='msgboard.Message', verbose_name='回复'),
        ),
    ]
