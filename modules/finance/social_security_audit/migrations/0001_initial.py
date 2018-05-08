# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialSecurityAudit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u59d3\u540d')),
                ('identity_card_number', models.CharField(max_length=18, verbose_name='\u8eab\u4efd\u8bc1\u53f7')),
                ('social_security_date', models.DateField(verbose_name='\u793e\u4fdd\u6708\u4efd')),
                ('social_security_billing', models.PositiveIntegerField(null=True, verbose_name='\u793e\u4fdd\u7ed3\u7b97', blank=True)),
                ('social_security_outlay', models.PositiveIntegerField(null=True, verbose_name='\u793e\u4fdd\u652f\u51fa', blank=True)),
                ('social_security_balance', models.CharField(max_length=1, verbose_name='\u793e\u4fdd\u5e73\u8861', choices=[(b'1', '\u5e73\u8861'), (b'2', '\u76c8\u4f59'), (b'3', '\u4e8f\u635f')])),
                ('provident_fund_billing', models.PositiveIntegerField(null=True, verbose_name='\u516c\u79ef\u91d1\u7ed3\u7b97', blank=True)),
                ('provident_fund_outlay', models.PositiveIntegerField(null=True, verbose_name='\u516c\u79ef\u91d1\u652f\u51fa', blank=True)),
                ('provident_fund_balance', models.CharField(max_length=1, verbose_name='\u516c\u79ef\u91d1\u5e73\u8861', choices=[(b'1', '\u5e73\u8861'), (b'2', '\u76c8\u4f59'), (b'3', '\u4e8f\u635f')])),
                ('remark', models.CharField(max_length=255, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('employee', models.ForeignKey(verbose_name='\u5458\u5de5\u7f16\u53f7', blank=True, to='employee_info.Employee', null=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u793e\u4fdd\u5ba1\u6838',
                'permissions': (('browse_socialsecurityaudit', '\u6d4f\u89c8 \u793e\u4fdd\u5ba1\u6838'), ('export_socialsecurityaudit', '\u5bfc\u51fa \u793e\u4fdd\u5ba1\u6838')),
            },
        ),
    ]
