# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayrollDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='\u59d3\u540d')),
                ('identity_card_number', models.CharField(max_length=18, verbose_name='\u8eab\u4efd\u8bc1\u53f7')),
                ('settle_accounts_month', models.DateField(verbose_name='\u7ed3\u7b97\u6708\u4efd')),
                ('wages_should_be', models.PositiveIntegerField(null=True, verbose_name='\u5e94\u53d1\u5de5\u8d44', blank=True)),
                ('person_social_security', models.PositiveIntegerField(null=True, verbose_name='\u4e2a\u4eba\u793e\u4fdd', blank=True)),
                ('person_provident_fund', models.PositiveIntegerField(null=True, verbose_name='\u4e2a\u4eba\u516c\u79ef\u91d1', blank=True)),
                ('pre_tax_adjustment', models.PositiveIntegerField(null=True, verbose_name='\u7a0e\u524d\u8c03\u6574', blank=True)),
                ('pre_tax_wage', models.PositiveIntegerField(null=True, verbose_name='\u7a0e\u524d\u5de5\u8d44', blank=True)),
                ('tax', models.PositiveIntegerField(null=True, verbose_name='\u4e2a\u7a0e', blank=True)),
                ('tax_rate', models.PositiveIntegerField(null=True, verbose_name='\u7a0e\u7387', blank=True)),
                ('quick_deduction', models.PositiveIntegerField(null=True, verbose_name='\u901f\u7b97\u6263\u9664\u6570', blank=True)),
                ('tax_adjustments', models.PositiveIntegerField(null=True, verbose_name='\u7a0e\u540e\u8c03\u6574', blank=True)),
                ('real_hair_wage', models.PositiveIntegerField(null=True, verbose_name='\u5b9e\u53d1\u5de5\u8d44', blank=True)),
                ('social_security_unit', models.PositiveIntegerField(null=True, verbose_name='\u793e\u4fdd\u5355\u4f4d', blank=True)),
                ('provident_fund_unit', models.PositiveIntegerField(null=True, verbose_name='\u516c\u79ef\u91d1\u5355\u4f4d', blank=True)),
                ('social_security_pay_unit', models.PositiveIntegerField(null=True, verbose_name='\u793e\u4fdd\u8865\u7f34\u5355\u4f4d', blank=True)),
                ('provident_fund_pay_unit', models.PositiveIntegerField(null=True, verbose_name='\u516c\u79ef\u91d1\u8865\u7f34\u5355\u4f4d', blank=True)),
                ('social_security_provident_fund_sum_unit', models.PositiveIntegerField(null=True, verbose_name='\u793e\u4fdd+\u516c\u79ef\u91d1\u5408\u8ba1\u5355\u4f4d', blank=True)),
                ('employer', models.PositiveIntegerField(null=True, verbose_name='\u96c7\u4e3b/\u5546\u4fdd/\u610f\u5916\u9669', blank=True)),
                ('security_for_disabled', models.PositiveIntegerField(null=True, verbose_name='\u6b8b\u75be\u4eba\u4fdd\u969c\u91d1', blank=True)),
                ('management_fee', models.PositiveIntegerField(null=True, verbose_name='\u7ba1\u7406\u8d39', blank=True)),
                ('total', models.PositiveIntegerField(null=True, verbose_name='\u5408\u8ba1', blank=True)),
                ('remark', models.CharField(max_length=256, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('project_name', models.ForeignKey(related_name='payroll_detal_project', verbose_name='\u9879\u76ee\u540d\u79f0', to='project_manage.Project')),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_payrolldetail', '\u6d4f\u89c8 \u85aa\u8d44\u660e\u7ec6'),),
                'verbose_name': '\u85aa\u8d44\u660e\u7ec6',
            },
        ),
        migrations.AlterIndexTogether(
            name='payrolldetail',
            index_together=set([('project_name', 'settle_accounts_month')]),
        ),
    ]
