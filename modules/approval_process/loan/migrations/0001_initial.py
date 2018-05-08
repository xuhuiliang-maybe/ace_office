# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
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
                ('money', models.PositiveIntegerField(default=0, help_text='\u7533\u8bf7\u5907\u7528\u91d1\u5177\u4f53\u91d1\u989d', verbose_name='\u7533\u8bf7\u91d1\u989d')),
                ('borrowing_date', models.DateField(help_text='\u80fd\u62ff\u5230\u5907\u7528\u91d1\u65f6\u95f4', verbose_name='\u501f\u6b3e\u65e5')),
                ('repayment_date', models.DateField(verbose_name='\u8fd8\u6b3e\u65e5')),
                ('apply_user', models.ForeignKey(related_name='loan_apply_user', verbose_name='\u7533\u8bf7\u4eba', to=settings.AUTH_USER_MODEL)),
                ('handle_user', models.ForeignKey(related_name='loan_handle_user', verbose_name='\u5ba1\u6279\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_loan', '\u6d4f\u89c8 \u5907\u7528\u91d1'),),
                'verbose_name': '\u5907\u7528\u91d1',
            },
        ),
        migrations.CreateModel(
            name='LoanBudgetDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_range', models.CharField(help_text='\u4e34\u65f6\u5de5\u9884\u7b97\u660e\u7ec6', max_length=256, verbose_name='\u65e5\u671f')),
                ('days', models.PositiveIntegerField(default=0, verbose_name='\u5929\u6570')),
                ('daily_number', models.PositiveIntegerField(default=0, verbose_name='\u6bcf\u5929\u4eba\u6570')),
                ('hours_per_day', models.PositiveIntegerField(default=0, verbose_name='\u6bcf\u5929\u4eba\u5747\u5de5\u65f6')),
                ('hourly_wage', models.PositiveIntegerField(default=0, verbose_name='\u5c0f\u65f6\u5de5\u8d44')),
                ('meals_per_capita', models.PositiveIntegerField(default=0, verbose_name='\u4eba\u5747\u9910\u8d39')),
                ('traffic_fee', models.PositiveIntegerField(default=0, verbose_name='\u4ea4\u901a\u8d39')),
                ('temporary_total', models.PositiveIntegerField(default=0, verbose_name='\u4e34\u65f6\u5de5\u9884\u7b97\u5408\u8ba1', editable=False)),
                ('amount', models.PositiveIntegerField(default=0, help_text='\u5176\u4ed6\u9884\u7b97\u660e\u7ec6', verbose_name='\u6570\u91cf')),
                ('unit_price', models.PositiveIntegerField(default=0, verbose_name='\u5355\u4ef7')),
                ('other_total', models.PositiveIntegerField(default=0, verbose_name='\u5176\u4ed6\u9884\u7b97\u5408\u8ba1', editable=False)),
                ('all_total', models.PositiveIntegerField(default=0, help_text='\u5176\u4ed6\u9884\u7b97\u660e\u7ec6', verbose_name='\u603b\u8ba1', editable=False)),
                ('applicants', models.ForeignKey(related_name='LoanBudgetDetails', editable=False, to='loan.Loan', verbose_name='\u5907\u7528\u91d1\u7533\u8bf7')),
            ],
            options={
                'verbose_name': '\u5907\u7528\u91d1\u8d39\u7528\u9884\u7b97\u660e\u7ec6',
            },
        ),
        migrations.AlterIndexTogether(
            name='loan',
            index_together=set([('title', 'apply_user')]),
        ),
    ]
