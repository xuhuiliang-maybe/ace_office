# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dict_table', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u7533\u8bf7\u6807\u9898')),
                ('note', models.TextField(max_length=256, verbose_name='\u7533\u8bf7\u8bf4\u660e')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u7533\u8bf7\u65f6\u95f4')),
                ('handle_date', models.DateTimeField(null=True, verbose_name='\u5ba1\u6279\u65f6\u95f4', blank=True)),
                ('reason', models.CharField(max_length=100, verbose_name='\u5ba1\u6279\u56de\u590d', blank=True)),
                ('status', models.CharField(default=b'1', max_length=1, verbose_name='\u5ba1\u6279\u72b6\u6001', choices=[(b'1', '\u5f85\u5ba1\u6279'), (b'2', '\u901a\u8fc7'), (b'3', '\u62d2\u7edd')])),
                ('apply_types', models.CharField(max_length=1, null=True, verbose_name='\u7533\u8bf7\u7c7b\u578b', choices=[(b'1', '\u8bf7\u5047'), (b'2', '\u5907\u7528\u91d1'), (b'3', '\u62a5\u9500\u4e0e\u9500\u8d26'), (b'4', '\u5de5\u8d44\u4e0e\u804c\u4f4d\u8c03\u6574'), (b'5', '\u5de5\u8d44\u8865\u53d1\u7533\u8bf7'), (b'6', '\u7ed3\u7b97\u4e0e\u53d1\u85aa'), (b'7', '\u7ba1\u7406\u4eba\u5458\u9700\u6c42\u4e0e\u79bb\u804c'), (b'8', '\u4e34\u65f6\u5de5\u9500\u8d26\u4e0e\u5f00\u7968'), (b'9', '\u5f85\u62db\u7ed3\u7b97\u4e0e\u9500\u8d26')])),
                ('remark1', models.CharField(max_length=256, verbose_name='\u5907\u6ce81', blank=True)),
                ('remark2', models.CharField(max_length=256, verbose_name='\u5907\u6ce82', blank=True)),
                ('begin_date', models.DateField(verbose_name='\u8bf7\u5047\u8d77\u59cb\u65f6\u95f4')),
                ('end_date', models.DateField(verbose_name='\u8bf7\u5047\u7ec8\u6b62\u65f6\u95f4')),
                ('apply_user', models.ForeignKey(related_name='leave_apply_user', verbose_name='\u7533\u8bf7\u4eba', to=settings.AUTH_USER_MODEL)),
                ('handle_user', models.ForeignKey(related_name='leave_handle_user', verbose_name='\u5ba1\u6279\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('leave_type', models.ManyToManyField(help_text='\u6309\u4f4f \u201dControl\u201c\uff0c\u6216\u8005Mac\u4e0a\u7684 \u201cCommand\u201d\uff0c\u53ef\u4ee5\u9009\u62e9\u591a\u4e2a\u3002', to='dict_table.LeaveType', verbose_name='\u8bf7\u5047\u7c7b\u578b', blank=True)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_leave', '\u6d4f\u89c8 \u8bf7\u5047'),),
                'verbose_name': '\u8bf7\u5047',
            },
        ),
        migrations.AlterIndexTogether(
            name='leave',
            index_together=set([('title', 'apply_user')]),
        ),
    ]
