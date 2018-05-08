# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingPrePay',
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
                ('billingprepay_month', models.DateField(verbose_name='\u7ed3\u7b97\u4e0e\u53d1\u85aa\u6708\u4efd')),
                ('billing_date_start', models.DateField(null=True, verbose_name='\u7ed3\u7b97\u5468\u671f\u8d77\u59cb', blank=True)),
                ('billing_date_end', models.DateField(null=True, verbose_name='\u7ed3\u7b97\u5468\u671f\u7ec8\u6b62', blank=True)),
                ('billing_content', models.CharField(max_length=255, null=True, verbose_name='\u7ed3\u7b97\u5185\u5bb9', blank=True)),
                ('main_business_income', models.PositiveIntegerField(verbose_name='\u4e3b\u8425\u4e1a\u6536\u5165', null=True, editable=False, blank=True)),
                ('management_fee', models.PositiveIntegerField(null=True, verbose_name='\u7ba1\u7406\u8d39', blank=True)),
                ('wage_receive', models.PositiveIntegerField(null=True, verbose_name='\u5de5\u8d44(\u6536)', blank=True)),
                ('social_security_receive', models.PositiveIntegerField(null=True, verbose_name='\u793e\u4fdd(\u6536)', blank=True)),
                ('provident_fund_receive', models.PositiveIntegerField(null=True, verbose_name='\u516c\u79ef\u91d1(\u6536)', blank=True)),
                ('union_fee_receive', models.PositiveIntegerField(null=True, verbose_name='\u5de5\u4f1a\u8d39(\u6536)', blank=True)),
                ('disablement_gold', models.PositiveIntegerField(null=True, verbose_name='\u6b8b\u4fdd\u91d1', blank=True)),
                ('shuttle_fee_receive', models.PositiveIntegerField(null=True, verbose_name='\u73ed\u8f66\u8d39(\u6536)', blank=True)),
                ('meals_receive', models.PositiveIntegerField(null=True, verbose_name='\u9910\u8d39(\u6536)', blank=True)),
                ('dormitory_fee_receive', models.PositiveIntegerField(null=True, verbose_name='\u5bbf\u820d\u8d39(\u6536)', blank=True)),
                ('daily_receive', models.PositiveIntegerField(null=True, verbose_name='\u5546\u62a5(\u6536)', blank=True)),
                ('compensate_reparation_receive', models.PositiveIntegerField(null=True, verbose_name='\u507f/\u8d54\u507f\u91d1(\u6536)', blank=True)),
                ('bonus_receive', models.PositiveIntegerField(null=True, verbose_name='\u5956\u91d1\u7c7b(\u6536)', blank=True)),
                ('other_receive', models.PositiveIntegerField(null=True, verbose_name='\u5176\u4ed6\u6536\u5165', blank=True)),
                ('grant_total', models.PositiveIntegerField(verbose_name='\u53d1\u653e\u603b\u989d', null=True, editable=False, blank=True)),
                ('ccb', models.PositiveIntegerField(null=True, verbose_name='\u5efa\u884c', blank=True)),
                ('merchants_bank', models.PositiveIntegerField(null=True, verbose_name='\u62db\u884c', blank=True)),
                ('icbc', models.PositiveIntegerField(null=True, verbose_name='\u5de5\u884c', blank=True)),
                ('other_bank', models.PositiveIntegerField(null=True, verbose_name='\u5176\u4ed6\u94f6\u884c', blank=True)),
                ('apply_user', models.ForeignKey(related_name='billing_pre_pay_apply_user', verbose_name='\u7533\u8bf7\u4eba', to=settings.AUTH_USER_MODEL)),
                ('handle_user', models.ForeignKey(related_name='billing_pre_pay_handle_user', verbose_name='\u5ba1\u6279\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('project_name', models.ForeignKey(verbose_name='\u7ed3\u7b97\u9879\u76ee\u540d\u79f0', to='project_manage.Project')),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_billingprepay', '\u6d4f\u89c8 \u7ed3\u7b97\u4e0e\u53d1\u85aa'),),
                'verbose_name': '\u7ed3\u7b97\u4e0e\u53d1\u85aa',
            },
        ),
        migrations.AlterIndexTogether(
            name='billingprepay',
            index_together=set([('title', 'apply_user')]),
        ),
    ]
