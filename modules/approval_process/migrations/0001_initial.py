# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingApproval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('apply_type', models.CharField(max_length=1, null=True, verbose_name='\u7533\u8bf7\u7c7b\u578b', choices=[(b'1', '\u8bf7\u5047'), (b'2', '\u5907\u7528\u91d1'), (b'3', '\u62a5\u9500\u4e0e\u9500\u8d26'), (b'4', '\u5de5\u8d44\u4e0e\u804c\u4f4d\u8c03\u6574'), (b'5', '\u5de5\u8d44\u8865\u53d1\u7533\u8bf7'), (b'6', '\u7ed3\u7b97\u4e0e\u53d1\u85aa'), (b'7', '\u7ba1\u7406\u4eba\u5458\u9700\u6c42\u4e0e\u79bb\u804c'), (b'8', '\u4e34\u65f6\u5de5\u9500\u8d26\u4e0e\u5f00\u7968'), (b'9', '\u5f85\u62db\u7ed3\u7b97\u4e0e\u9500\u8d26')])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u5f85\u5ba1\u6279\u7533\u8bf7\u4fe1\u606f',
                'permissions': (('browse_pendingapproval', '\u6d4f\u89c8 \u5f85\u5ba1\u6279\u4fe1\u606f'),),
            },
        ),
    ]
