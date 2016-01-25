# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0003_auto_20160122_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='sourceid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='network',
            name='targetid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='network',
            name='source',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='network',
            name='target',
            field=models.CharField(max_length=100),
        ),
    ]
