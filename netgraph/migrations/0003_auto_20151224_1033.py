# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0002_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='network',
            name='weight',
            field=models.CharField(max_length=20),
        ),
    ]
