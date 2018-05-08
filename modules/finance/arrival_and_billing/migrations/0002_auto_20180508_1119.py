# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrival_and_billing', '0001_initial'),
        ('project_manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrivalandbilling',
            name='project_name',
            field=models.ForeignKey(related_name='arrivalandbilling', verbose_name='\u9879\u76ee\u540d\u79f0', to='project_manage.Project'),
        ),
        migrations.AlterIndexTogether(
            name='arrivalandbilling',
            index_together=set([('project_name',)]),
        ),
    ]
