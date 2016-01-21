# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0007_auto_20160120_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='node1attr',
            field=models.CharField(default=datetime.datetime(2016, 1, 20, 7, 23, 57, 234190, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='links',
            name='node2attr',
            field=models.CharField(default=datetime.datetime(2016, 1, 20, 7, 24, 3, 763266, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='links',
            name='node1',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='links',
            name='node2',
            field=models.CharField(max_length=100),
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
