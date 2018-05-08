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
            name='TemporaryWriteOffsBilling',
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
                ('billing_month', models.DateField(null=True, verbose_name='\u7ed3\u7b97\u6708\u4efd', blank=True)),
                ('billing_date_start', models.DateField(null=True, verbose_name='\u7ed3\u7b97\u5468\u671f\u8d77\u59cb', blank=True)),
                ('billing_date_end', models.DateField(null=True, verbose_name='\u7ed3\u7b97\u5468\u671f\u7ec8\u6b62', blank=True)),
                ('billing_content', models.CharField(max_length=255, null=True, verbose_name='\u7ed3\u7b97\u5185\u5bb9', blank=True)),
                ('billing_type', models.CharField(blank=True, max_length=1, null=True, verbose_name='\u7ed3\u7b97\u65b9\u5f0f', choices=[(b'1', '\u5355\u72ec\u7ed3\u7b97'), (b'2', '\u5408\u5e76\u7ed3\u7b97')])),
                ('main_business_income', models.PositiveIntegerField(verbose_name='\u4e3b\u8425\u4e1a\u6536\u5165', null=True, editable=False, blank=True)),
                ('management_fee', models.PositiveIntegerField(null=True, verbose_name='\u7ba1\u7406\u8d39', blank=True)),
                ('wage_receive', models.PositiveIntegerField(null=True, verbose_name='\u5de5\u8d44(\u6536)', blank=True)),
                ('shuttle_fee_receive', models.PositiveIntegerField(null=True, verbose_name='\u73ed\u8f66\u8d39(\u6536)', blank=True)),
                ('meals_receive', models.PositiveIntegerField(null=True, verbose_name='\u9910\u8d39(\u6536)', blank=True)),
                ('dormitory_fee_receive', models.PositiveIntegerField(null=True, verbose_name='\u5bbf\u820d\u8d39(\u6536)', blank=True)),
                ('daily_receive', models.PositiveIntegerField(null=True, verbose_name='\u5546\u62a5(\u6536)', blank=True)),
                ('compensate_reparation_receive', models.PositiveIntegerField(null=True, verbose_name='\u8d54\u4ed8\u6b3e(\u6536)', blank=True)),
                ('actual_outlay', models.PositiveIntegerField(null=True, verbose_name='\u5b9e\u9645\u652f\u51fa', blank=True)),
                ('main_business_outlay', models.PositiveIntegerField(null=True, verbose_name='\u4e3b\u8425\u4e1a\u652f\u51fa', blank=True)),
                ('wage_outlay', models.PositiveIntegerField(null=True, verbose_name='\u5de5\u8d44(\u4ed8)', blank=True)),
                ('shuttle_fee_outlay', models.PositiveIntegerField(null=True, verbose_name='\u73ed\u8f66\u8d39(\u4ed8)', blank=True)),
                ('meals_outlay', models.PositiveIntegerField(null=True, verbose_name='\u9910\u8d39(\u4ed8)', blank=True)),
                ('daily_outlay', models.PositiveIntegerField(null=True, verbose_name='\u5546\u62a5(\u4ed8)', blank=True)),
                ('compensate_reparation_outlay', models.PositiveIntegerField(null=True, verbose_name='\u8d54\u507f/\u8865\u507f\u91d1(\u4ed8)', blank=True)),
                ('borrow_loan', models.PositiveIntegerField(null=True, verbose_name='\u5df2\u501f\u5907\u7528\u91d1', blank=True)),
                ('difference', models.PositiveIntegerField(default=0, verbose_name='\u5dee\u989d', editable=False)),
                ('is_billing', models.CharField(blank=True, max_length=1, null=True, verbose_name='\u662f\u5426\u5f00\u7968', choices=[(b'1', '\u662f'), (b'2', '\u5426')])),
                ('apply_user', models.ForeignKey(related_name='temporary_write_offs_billing_apply_user', verbose_name='\u7533\u8bf7\u4eba', to=settings.AUTH_USER_MODEL)),
                ('handle_user', models.ForeignKey(related_name='temporary_write_offs_billing_handle_user', verbose_name='\u5ba1\u6279\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('project_name', models.ForeignKey(verbose_name='\u9879\u76ee\u540d\u79f0', to='project_manage.Project', null=True)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('browse_temporary_write_offs_billing', '\u6d4f\u89c8 \u4e34\u65f6\u5de5\u9500\u8d26\u4e0e\u5f00\u7968'),),
                'verbose_name': '\u4e34\u65f6\u5de5\u9500\u8d26\u4e0e\u5f00\u7968',
            },
        ),
        migrations.CreateModel(
            name='TemporaryWriteOffsBillingDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u59d3\u540d')),
                ('sex', models.CharField(blank=True, help_text='\u9009\u586b\uff0c\u53ef\u7531\u8eab\u4efd\u8bc1\u53f7\u8ba1\u7b97', max_length=2, verbose_name='\u6027\u522b', choices=[(b'M', '\u7537'), (b'F', '\u5973')])),
                ('identity_card_number', models.CharField(max_length=18, verbose_name='\u8eab\u4efd\u8bc1\u53f7')),
                ('phone_number', models.CharField(max_length=100, verbose_name='\u8054\u7cfb\u7535\u8bdd', blank=True)),
                ('start_work_date', models.DateField(null=True, verbose_name='\u5f00\u59cb\u5de5\u4f5c\u65e5', blank=True)),
                ('end_work_date', models.DateField(null=True, verbose_name='\u7ed3\u675f\u5de5\u4f5c\u65e5', blank=True)),
                ('work_days', models.PositiveIntegerField(null=True, verbose_name='\u5de5\u4f5c\u5929\u6570', blank=True)),
                ('hours', models.PositiveIntegerField(null=True, verbose_name='\u5c0f\u65f6\u6570', blank=True)),
                ('amount_of_payment', models.PositiveIntegerField(null=True, verbose_name='\u53d1\u653e\u91d1\u989d', blank=True)),
                ('release_time', models.DateField(null=True, verbose_name='\u53d1\u653e\u65f6\u95f4', blank=True)),
                ('remark1', models.CharField(max_length=256, verbose_name='\u5907\u6ce81', blank=True)),
                ('applicants', models.ForeignKey(related_name='temporarywriteoffsbillingdetails', editable=False, to='temporary_write_offs_billing.TemporaryWriteOffsBilling', verbose_name='\u4e34\u65f6\u5de5\u9500\u8d26\u4e0e\u5f00\u7968\u7533\u8bf7')),
                ('project_name', models.ForeignKey(related_name='temporary', verbose_name='\u9879\u76ee\u540d\u79f0', blank=True, to='project_manage.Project', null=True)),
                ('recruitment_attache', models.ForeignKey(related_name='temporary_user_recruitment_attache', verbose_name='\u62db\u8058\u4eba\u5458', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('release_user', models.ForeignKey(related_name='temporary_release_user', verbose_name='\u53d1\u653e\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u4e34\u65f6\u5de5\u9500\u8d26\u4e0e\u5f00\u7968\u660e\u7ec6',
            },
        ),
        migrations.AlterIndexTogether(
            name='temporarywriteoffsbilling',
            index_together=set([('title', 'apply_user')]),
        ),
    ]
