# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Purview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u83dc\u5355\u6d4f\u89c8\u6743\u9650',
                'permissions': (('browse_index', '\u6d4f\u89c8 \u6211\u7684\u4e3b\u9875'), ('browse_mysite', '\u6d4f\u89c8 \u6211\u7684\u5730\u76d8'), ('browse_personal', '\u6d4f\u89c8 \u6211\u7684\u4e2a\u4eba\u4fe1\u606f'), ('browse_organizational', '\u6d4f\u89c8 \u7ec4\u7ec7\u67b6\u6784'), ('browse_structure', '\u6d4f\u89c8 \u7ec4\u7ec7\u67b6\u6784\u56fe'), ('browse_project_manage', '\u6d4f\u89c8 \u9879\u76ee\u7ba1\u7406'), ('browse_user', '\u6d4f\u89c8 \u7ba1\u7406\u4eba\u5458'), ('browse_employee_manage', '\u6d4f\u89c8 \u5458\u5de5\u7ba1\u7406'), ('browse_socialsecurity', '\u6d4f\u89c8 \u793e\u4fdd\u798f\u5229'), ('browse_recruitment', '\u6d4f\u89c8 \u62db\u8058\u7ba1\u7406'), ('browse_month_entry_job_details', '\u6d4f\u89c8 \u5f53\u6708\u5165\u804c\u62db\u8058\u660e\u7ec6'), ('browse_individual_job', '\u6d4f\u89c8 \u4e2a\u4eba\u62db\u8058'), ('browse_job_statistic', '\u6d4f\u89c8 \u62db\u8058\u7edf\u8ba1'), ('export_job_statistic', '\u5bfc\u51fa \u62db\u8058\u7edf\u8ba1'), ('browse_approval', '\u6d4f\u89c8 \u5ba1\u6279\u6d41\u7a0b'), ('browse_apply_info_template', '\u6d4f\u89c8 \u7533\u8bf7\u4fe1\u606f\u6a21\u677f'), ('browse_approval_pending', '\u6d4f\u89c8 \u5f85\u5ba1\u6279\u4fe1\u606f'), ('browse_qualityassurance_manage', '\u6d4f\u89c8 \u4eba\u4e8b\u64cd\u4f5c\u8d28\u91cf'), ('browse_qualityassurance_gather', '\u6d4f\u89c8 \u64cd\u4f5c\u8d28\u91cf\u6c47\u603b'), ('browse_system', '\u6d4f\u89c8 \u7cfb\u7edf\u76f8\u5173'), ('browse_admin', '\u6d4f\u89c8 \u6743\u9650\u7ba1\u7406'), ('browse_dict', '\u6d4f\u89c8 \u5b57\u5178\u8868'), ('browse_payroll_manage', '\u6d4f\u89c8 \u85aa\u8d44\u7ba1\u7406'), ('browse_finance', '\u6d4f\u89c8 \u8d22\u52a1\u7ba1\u7406'), ('browse_contract', '\u6d4f\u89c8 \u5408\u540c\u7ba1\u7406')),
            },
        ),
    ]
