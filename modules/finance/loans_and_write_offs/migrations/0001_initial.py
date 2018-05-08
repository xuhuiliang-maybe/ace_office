# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoansAndWriteOffs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_write_offs', models.PositiveIntegerField(null=True, verbose_name='\u9500\u8d26\u91d1\u989d', blank=True)),
                ('write_offs_date', models.DateField(null=True, verbose_name='\u9500\u8d26\u65f6\u95f4', blank=True)),
                ('remark', models.CharField(max_length=256, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('loan', models.ForeignKey(related_name='loansandwriteoffs', verbose_name='\u5907\u7528\u91d1', blank=True, to='loan.Loan', null=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '\u501f\u6b3e\u4e0e\u9500\u8d26',
                'permissions': (('browse_loansandwriteoffs', '\u6d4f\u89c8 \u501f\u6b3e\u4e0e\u9500\u8d26'), ('export_loansandwriteoffs', '\u5bfc\u51fa \u501f\u6b3e\u4e0e\u9500\u8d26')),
            },
        ),
    ]
