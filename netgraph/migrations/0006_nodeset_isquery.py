# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0005_auto_20160125_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodeset',
            name='isquery',
            field=models.BooleanField(default=False),
        ),
    ]
