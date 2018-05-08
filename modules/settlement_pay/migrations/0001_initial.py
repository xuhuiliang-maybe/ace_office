# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pay_month', models.DateField(null=True, verbose_name='\u5de5\u8d44\u6708\u4efd', blank=True)),
                ('post_salary', models.FloatField(null=True, verbose_name='\u5c97\u4f4d\u5de5\u8d44', blank=True)),
                ('float_salary', models.FloatField(null=True, verbose_name='\u6d6e\u52a8\u5de5\u8d44', blank=True)),
                ('full_award', models.FloatField(null=True, verbose_name='\u5168\u52e4\u5956', blank=True)),
                ('award', models.FloatField(null=True, verbose_name='\u5956\u91d1', blank=True)),
                ('hous_subsidy', models.FloatField(null=True, verbose_name='\u4f4f\u623f\u8865\u8d34', blank=True)),
                ('traffic_subsidy', models.FloatField(null=True, verbose_name='\u4ea4\u901a\u8865\u8d34', blank=True)),
                ('commodity_subsidy', models.FloatField(null=True, verbose_name='\u7269\u4ef7\u8865\u8d34', blank=True)),
                ('food_subsidy', models.FloatField(null=True, verbose_name='\u4f19\u98df\u8865\u8d34', blank=True)),
                ('time_salary', models.FloatField(null=True, verbose_name='\u8ba1\u65f6\u5de5\u8d44', blank=True)),
                ('piece_salary', models.FloatField(null=True, verbose_name='\u8ba1\u4ef6\u5de5\u8d44', blank=True)),
                ('deducty_salary', models.FloatField(null=True, verbose_name='\u5e94\u6263\u5de5\u8d44', blank=True)),
                ('remark1', models.CharField(max_length=256, verbose_name='\u5907\u6ce81', blank=True)),
                ('remark2', models.CharField(max_length=256, verbose_name='\u5907\u6ce82', blank=True)),
                ('remark3', models.CharField(max_length=256, verbose_name='\u5907\u6ce83', blank=True)),
                ('remark4', models.CharField(max_length=256, verbose_name='\u5907\u6ce84', blank=True)),
                ('remark5', models.CharField(max_length=256, verbose_name='\u5907\u6ce85', blank=True)),
                ('employee', models.ForeignKey(verbose_name='\u5458\u5de5\u7f16\u53f7', to='employee_info.Employee')),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_payroll', '\u6d4f\u89c8 \u7ed3\u7b97\u53d1\u85aa'),),
                'verbose_name': '\u7ed3\u7b97\u53d1\u85aa',
            },
        ),
        migrations.AlterIndexTogether(
            name='payroll',
            index_together=set([('employee', 'pay_month')]),
        ),
    ]
