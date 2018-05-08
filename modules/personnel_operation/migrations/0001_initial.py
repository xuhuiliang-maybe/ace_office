# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departments', '0001_initial'),
        ('dict_table', '0001_initial'),
        ('project_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QualityAssurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index_items', models.CharField(max_length=1, verbose_name='\u6307\u6807\u9879', choices=[(b'1', '\u5458\u5de5\u4fe1\u606f'), (b'2', '\u5408\u540c'), (b'3', '\u5de5\u8d44'), (b'4', '\u793e\u4fdd'), (b'5', '\u8d44\u6599\u90ae\u5bc4'), (b'6', '\u53d1\u51fd'), (b'7', '\u529e\u5361\u8d44\u6599'), (b'8', '\u5176\u4ed6')])),
                ('problems_items', models.CharField(max_length=300, verbose_name='\u95ee\u9898\u9879')),
                ('problems_explain', models.TextField(max_length=300, verbose_name='\u95ee\u9898\u8bf4\u660e')),
                ('error_number', models.PositiveIntegerField(default=1, verbose_name='\u64cd\u4f5c\u9519\u8bef\u6570')),
                ('error_date', models.DateField(verbose_name='\u95ee\u9898\u65e5\u671f')),
                ('improve_time', models.PositiveIntegerField(help_text='\u5355\u4f4d\uff1a\u5929', verbose_name='\u6539\u5584\u65f6\u9650')),
                ('improve_date', models.DateField(verbose_name='\u6539\u5584\u65e5\u671f')),
                ('remark', models.CharField(max_length=256, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('remark1', models.CharField(max_length=256, verbose_name='\u5907\u6ce81', blank=True)),
                ('remark2', models.CharField(max_length=256, verbose_name='\u5907\u6ce82', blank=True)),
                ('remark3', models.CharField(max_length=256, verbose_name='\u5907\u6ce83', blank=True)),
                ('remark4', models.CharField(max_length=256, verbose_name='\u5907\u6ce84', blank=True)),
                ('create_user', models.ForeignKey(related_name='quality_create_user', verbose_name='\u521b\u5efa\u4eba', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(verbose_name='\u670d\u52a1\u90e8\u95e8', blank=True, to='departments.Department', null=True)),
                ('improve_status', models.ForeignKey(verbose_name='\u6539\u5584\u72b6\u6001', to='dict_table.ImproveStatus')),
                ('project_id', models.ForeignKey(related_name='quality_project_name', verbose_name='\u9879\u76ee\u540d\u79f0', to='project_manage.Project')),
                ('provider', models.ForeignKey(related_name='quality_provider', verbose_name='\u6570\u636e\u63d0\u4f9b\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_qualityassurance', '\u6d4f\u89c8 \u4e2a\u4eba\u64cd\u4f5c\u8d28\u91cf'),),
                'verbose_name': '\u4e2a\u4eba\u64cd\u4f5c\u8d28\u91cf',
            },
        ),
        migrations.AlterIndexTogether(
            name='qualityassurance',
            index_together=set([('improve_status', 'error_date')]),
        ),
    ]
