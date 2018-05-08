# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('employee_info', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dict_table', '0001_initial'),
        ('project_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inorout', models.CharField(default=b'1', max_length=100, verbose_name='\u6536\u652f\u7c7b\u578b', choices=[(b'1', '\u652f\u51fa'), (b'2', '\u6536\u5165')])),
                ('note', models.CharField(max_length=100, verbose_name='\u7533\u8bf7\u8bf4\u660e')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u7533\u8bf7\u65f6\u95f4')),
                ('handle_user', models.CharField(max_length=100, verbose_name='\u5ba1\u6279\u4eba', blank=True)),
                ('handle_date', models.DateTimeField(null=True, verbose_name='\u5ba1\u6279\u65f6\u95f4', blank=True)),
                ('reason', models.CharField(max_length=100, verbose_name='\u5ba1\u6279\u56de\u590d', blank=True)),
                ('status', models.CharField(default=b'1', max_length=100, verbose_name='\u5ba1\u6279\u72b6\u6001', choices=[(b'1', '\u5f85\u5ba1\u6279'), (b'2', '\u901a\u8fc7'), (b'3', '\u62d2\u7edd')])),
                ('remark1', models.CharField(max_length=256, verbose_name='\u5907\u6ce81', blank=True)),
                ('remark2', models.CharField(max_length=256, verbose_name='\u5907\u6ce82', blank=True)),
                ('remark3', models.CharField(max_length=256, verbose_name='\u5907\u6ce83', blank=True)),
                ('remark4', models.CharField(max_length=256, verbose_name='\u5907\u6ce84', blank=True)),
                ('remark5', models.CharField(max_length=256, verbose_name='\u5907\u6ce85', blank=True)),
                ('apply_user', models.ForeignKey(verbose_name='\u7533\u8bf7\u4eba', to=settings.AUTH_USER_MODEL)),
                ('emplyid', models.ForeignKey(related_name='expense_emp', verbose_name='\u5458\u5de5\u7f16\u53f7', blank=True, to='employee_info.Employee', null=True)),
                ('expensetype', models.ForeignKey(verbose_name='\u8d39\u7528\u7c7b\u578b', blank=True, to='dict_table.ExpenseType', null=True)),
                ('projectid', models.ForeignKey(related_name='expense_project', verbose_name='\u9879\u76ee\u540d\u79f0', blank=True, to='project_manage.Project', null=True)),
                ('userid', models.ForeignKey(related_name='expense_user', verbose_name='\u8d39\u7528\u8d1f\u8d23\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_expense', '\u6d4f\u89c8 \u8d39\u7528\u4fe1\u606f'),),
                'verbose_name': '\u8d39\u7528\u4fe1\u606f',
            },
        ),
        migrations.AlterIndexTogether(
            name='expense',
            index_together=set([('emplyid', 'projectid')]),
        ),
    ]
