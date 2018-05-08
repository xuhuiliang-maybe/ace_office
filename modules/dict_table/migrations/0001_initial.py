# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u6863\u6848\u7c7b\u578b\u4fe1\u606f',
                'permissions': (('browse_archivetype', '\u6d4f\u89c8 \u6863\u6848\u7c7b\u578b\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='BusinessInsuranceCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u5546\u4fdd\u516c\u53f8\u4fe1\u606f',
                'permissions': (('browse_businessinsurancecompany', '\u6d4f\u89c8 \u5546\u4fdd\u516c\u53f8\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='CompanySubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u516c\u53f8\u4e3b\u4f53\u4fe1\u606f',
                'permissions': (('browse_companysubject', '\u6d4f\u89c8 \u516c\u53f8\u4e3b\u4f53\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u5408\u540c\u7c7b\u578b\u4fe1\u606f',
                'permissions': (('browse_contracttype', '\u6d4f\u89c8 \u5408\u540c\u7c7b\u578b\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u65f6\u95f4\u5468\u671f\u4fe1\u606f',
                'permissions': (('browse_cycle', '\u6d4f\u89c8 \u65f6\u95f4\u5468\u671f\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u8d39\u7528\u7c7b\u578b\u4fe1\u606f',
                'permissions': (('browse_expensetype', '\u6d4f\u89c8 \u8d39\u7528\u7c7b\u578b\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='ImproveStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u6539\u5584\u72b6\u6001\u4fe1\u606f',
                'permissions': (('browse_improvestatus', '\u6d4f\u89c8 \u6539\u5584\u72b6\u6001\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='InvoiceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u53d1\u7968\u7c7b\u578b\u4fe1\u606f',
                'permissions': (('browse_invoicetype', '\u6d4f\u89c8 \u53d1\u7968\u7c7b\u578b\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='LeaveType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u8bf7\u5047\u7c7b\u578b',
                'permissions': (('browse_leavetype', '\u6d4f\u89c8 \u8bf7\u5047\u7c7b\u578b'),),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u5c97\u4f4d\u4fe1\u606f',
                'permissions': (('browse_position', '\u6d4f\u89c8 \u5c97\u4f4d\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='ProgressState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u9879\u76ee\u76ee\u524d\u72b6\u6001\u4fe1\u606f',
                'permissions': (('browse_progressstate', '\u6d4f\u89c8\u9879 \u76ee\u76ee\u524d\u72b6\u6001\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u9879\u76ee\u7c7b\u578b\u4fe1\u606f',
                'permissions': (('browse_projecttype', '\u6d4f\u89c8 \u9879\u76ee\u7c7b\u578b\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='SalesType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u9500\u552e\u7c7b\u578b\u4fe1\u606f',
                'permissions': (('browse_salestype', '\u6d4f\u89c8 \u9500\u552e\u7c7b\u578b\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='SocialSecurityAccountType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u793e\u4fdd\u8d26\u6237\u7c7b\u578b\u4fe1\u606f',
                'permissions': (('browse_socialsecurityaccounttype', '\u6d4f\u89c8 \u793e\u4fdd\u8d26\u6237\u7c7b\u578b\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='SocialSecurityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u793e\u4fdd\u9669\u79cd\u4fe1\u606f',
                'permissions': (('browse_socialsecuritytype', '\u6d4f\u89c8 \u793e\u4fdd\u9669\u79cd\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u79d1\u76ee\u4fe1\u606f',
                'permissions': (('browse_subject', '\u6d4f\u89c8 \u79d1\u76ee\u4fe1\u606f'),),
            },
        ),
        migrations.CreateModel(
            name='WageGrantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u540d\u79f0')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u5de5\u8d44\u53d1\u653e\u65b9\u5f0f\u4fe1\u606f',
                'permissions': (('browse_wagegranttype', '\u6d4f\u89c8 \u5de5\u8d44\u53d1\u653e\u65b9\u5f0f\u4fe1\u606f'),),
            },
        ),
    ]
