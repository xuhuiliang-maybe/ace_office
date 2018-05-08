# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='\u90e8\u95e8\u540d\u79f0')),
                ('parent_dept', models.PositiveIntegerField(default=1, verbose_name='\u4e0a\u7ea7\u90e8\u95e8')),
                ('apportion_type', models.CharField(default=b'1', max_length=1, verbose_name='\u5206\u644a\u7c7b\u578b', choices=[(b'1', '\u4e2a\u4eba\u5206\u644a'), (b'2', '\u90e8\u95e8\u5206\u644a'), (b'3', '\u516c\u53f8\u5206\u644a')])),
            ],
            options={
                'permissions': (('browse_department', '\u6d4f\u89c8 \u90e8\u95e8\u4fe1\u606f'),),
                'verbose_name': '\u90e8\u95e8\u4fe1\u606f',
            },
        ),
        migrations.AlterIndexTogether(
            name='department',
            index_together=set([('name',)]),
        ),
    ]
