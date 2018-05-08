# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departments', '0001_initial'),
        ('dict_table', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WriteOffs',
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
                ('writeoffs_total', models.PositiveIntegerField(default=0, verbose_name='\u62a5\u9500/\u9500\u8d26\u603b\u989d', editable=False)),
                ('borrow_imprest', models.PositiveIntegerField(default=0, verbose_name='\u5df2\u501f\u5907\u7528\u91d1')),
                ('imprest_explain', models.CharField(max_length=256, null=True, verbose_name='\u5907\u7528\u91d1\u8bf4\u660e', blank=True)),
                ('difference', models.PositiveIntegerField(default=0, verbose_name='\u5dee\u989d', editable=False)),
                ('writeoffs_type', models.CharField(blank=True, max_length=1, null=True, verbose_name='\u9500\u8d26\u7c7b\u578b', choices=[(b'1', '\u7968\u636e\u9500\u8d26'), (b'2', '\u7ed3\u7b97\u9500\u8d26'), (b'3', '\u5176\u4ed6\u9500\u8d26')])),
                ('remark', models.CharField(max_length=256, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('apply_user', models.ForeignKey(related_name='writeoffs_apply_user', verbose_name='\u7533\u8bf7\u4eba', to=settings.AUTH_USER_MODEL)),
                ('handle_user', models.ForeignKey(related_name='writeoffs_handle_user', verbose_name='\u5ba1\u6279\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_write_offs', '\u6d4f\u89c8 \u62a5\u9500\u4e0e\u9500\u8d26'),),
                'verbose_name': '\u62a5\u9500\u4e0e\u9500\u8d26',
            },
        ),
        migrations.CreateModel(
            name='WriteOffsDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_range', models.DateField(verbose_name='\u65e5\u671f')),
                ('money', models.PositiveIntegerField(default=0, verbose_name='\u91d1\u989d')),
                ('project_name', models.CharField(max_length=255, null=True, verbose_name='\u8d39\u7528\u9879\u76ee', blank=True)),
                ('cost_sharing', models.CharField(max_length=1, verbose_name='\u8d39\u7528\u5206\u644a\u65b9\u5f0f', choices=[(b'1', b'\xe9\xa1\xb9\xe7\x9b\xae\xe5\x88\x86\xe6\x91\x8a'), (b'2', b'\xe9\x83\xa8\xe9\x97\xa8\xe5\x88\x86\xe6\x91\x8a'), (b'3', b'\xe5\x85\xac\xe5\x8f\xb8\xe5\x88\x86\xe6\x91\x8a')])),
                ('cost_detail', models.TextField(max_length=300, verbose_name='\u8d39\u7528\u660e\u7ec6\u8bf4\u660e')),
                ('invoice_situation', models.TextField(max_length=300, verbose_name='\u53d1\u7968\u60c5\u51b5')),
                ('remark', models.CharField(max_length=256, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('applicants', models.ForeignKey(related_name='WriteOffsDetails', editable=False, to='write_offs.WriteOffs', verbose_name='\u62a5\u9500/\u9500\u8d26\u7533\u8bf7')),
                ('department', models.ForeignKey(verbose_name='\u8d39\u7528\u90e8\u95e8', to='departments.Department')),
                ('payee', models.ForeignKey(related_name='writeoffsdetail_payee', verbose_name='\u9886\u6b3e\u4eba', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(verbose_name='\u79d1\u76ee', to='dict_table.Subject')),
            ],
            options={
                'verbose_name': '\u62a5\u9500\u4e0e\u9500\u8d26\uff0c\u660e\u7ec6\u8868',
            },
        ),
        migrations.AlterIndexTogether(
            name='writeoffs',
            index_together=set([('title', 'apply_user')]),
        ),
    ]
