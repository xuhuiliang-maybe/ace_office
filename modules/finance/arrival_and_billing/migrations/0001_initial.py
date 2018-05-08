# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArrivalAndBilling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('settlement_date', models.DateField(verbose_name='\u7ed3\u7b97\u6708\u4efd')),
                ('settlement_amount_long', models.PositiveIntegerField(null=True, verbose_name='\u7ed3\u7b97\u91d1\u989d\uff08\u957f\u671f\u4e1a\u52a1\uff09', blank=True)),
                ('settlement_amount_snap', models.PositiveIntegerField(null=True, verbose_name='\u7ed3\u7b97\u91d1\u989d\uff08\u4e34\u65f6\u5de5\uff09', blank=True)),
                ('settlement_tatol', models.PositiveIntegerField(null=True, verbose_name='\u7ed3\u7b97\u5408\u8ba1', blank=True)),
                ('credited_amount_total', models.PositiveIntegerField(null=True, verbose_name='\u5230\u8d26\u91d1\u989d\u5408\u8ba1', blank=True)),
                ('credited_date', models.DateField(null=True, verbose_name='\u5230\u8d26\u65f6\u95f4', blank=True)),
                ('credited_state', models.CharField(blank=True, max_length=1, null=True, verbose_name='\u5230\u8d26\u60c5\u51b5', choices=[(b'1', '\u90e8\u5206\u5230\u8d26'), (b'2', '\u5168\u90e8\u5230\u8d26'), (b'3', '\u8d85\u989d\u5230\u8d26'), (b'4', '\u672a\u5230\u8d26')])),
                ('billing_amount_total', models.PositiveIntegerField(null=True, verbose_name='\u5f00\u7968\u91d1\u989d\u5408\u8ba1', blank=True)),
                ('billing_date', models.DateField(null=True, verbose_name='\u5f00\u7968\u65f6\u95f4', blank=True)),
                ('billing_state', models.CharField(blank=True, max_length=1, null=True, verbose_name='\u5f00\u7968\u60c5\u51b5', choices=[(b'1', '\u90e8\u5206\u5f00\u7968'), (b'2', '\u5168\u90e8\u5f00\u7968'), (b'3', '\u8d85\u989d\u5f00\u7968'), (b'4', '\u672a\u5f00\u7968')])),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_arrivalandbilling', '\u6d4f\u89c8 \u5230\u8d26\u4e0e\u5f00\u7968'), ('export_arrivalandbilling', '\u5bfc\u51fa \u5230\u8d26\u4e0e\u5f00\u7968')),
                'verbose_name': '\u5230\u8d26\u4e0e\u5f00\u7968',
            },
        ),
        migrations.CreateModel(
            name='BillingDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('billing_amount', models.PositiveIntegerField(null=True, verbose_name='\u5f00\u7968\u91d1\u989d', blank=True)),
                ('billing_date', models.DateField(verbose_name='\u5f00\u7968\u65f6\u95f4')),
                ('billing', models.ForeignKey(related_name='billingdetails', editable=False, to='arrival_and_billing.ArrivalAndBilling', verbose_name='\u5230\u8d26\u4e0e\u5f00\u7968')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u5f00\u7968\u660e\u7ec6',
            },
        ),
        migrations.CreateModel(
            name='CreditedDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credited_amount', models.PositiveIntegerField(null=True, verbose_name='\u5230\u8d26\u91d1\u989d', blank=True)),
                ('credited_date', models.DateField(verbose_name='\u5230\u8d26\u65f6\u95f4')),
                ('arrival', models.ForeignKey(related_name='crediteddetails', editable=False, to='arrival_and_billing.ArrivalAndBilling', verbose_name='\u5230\u8d26\u4e0e\u5f00\u7968')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u5230\u8d26\u660e\u7ec6',
            },
        ),
    ]
