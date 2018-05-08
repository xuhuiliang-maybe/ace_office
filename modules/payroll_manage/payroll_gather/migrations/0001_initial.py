# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PayrollGater',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u85aa\u8d44\u6c47\u603b',
                'permissions': (('browse_payrollgather', '\u6d4f\u89c8 \u85aa\u8d44\u6c47\u603b'), ('export_payrollgather', '\u5bfc\u51fa \u85aa\u8d44\u6c47\u603b')),
            },
        ),
    ]
