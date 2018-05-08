# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dept_verify', models.CharField(default=b'1', max_length=100, verbose_name='\u90e8\u95e8\u786e\u8ba4', choices=[(b'1', '\u672a\u786e\u8ba4'), (b'2', '\u786e\u8ba4')])),
                ('complete_verify', models.CharField(default=b'1', max_length=100, verbose_name='\u6700\u7ec8\u786e\u8ba4', choices=[(b'1', '\u672a\u786e\u8ba4'), (b'2', '\u786e\u8ba4')])),
                ('remark', models.CharField(max_length=200, verbose_name='\u5907\u6ce8', blank=True)),
                ('remark1', models.CharField(max_length=256, verbose_name='\u5907\u6ce81', blank=True)),
                ('remark2', models.CharField(max_length=256, verbose_name='\u5907\u6ce82', blank=True)),
                ('remark3', models.CharField(max_length=256, verbose_name='\u5907\u6ce83', blank=True)),
                ('remark4', models.CharField(max_length=256, verbose_name='\u5907\u6ce84', blank=True)),
                ('emplyid', models.ForeignKey(verbose_name='\u5458\u5de5\u7f16\u53f7', to='employee_info.Employee')),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_reduction', '\u6d4f\u89c8 \u51cf\u5458\u4fe1\u606f'),),
                'verbose_name': '\u51cf\u5458\u4fe1\u606f',
            },
        ),
        migrations.AlterIndexTogether(
            name='reduction',
            index_together=set([('emplyid',)]),
        ),
    ]
