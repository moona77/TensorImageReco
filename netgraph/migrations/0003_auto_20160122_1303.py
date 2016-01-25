# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0002_auto_20160122_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='node1',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='links',
            name='node2',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='network',
            name='source',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='network',
            name='target',
            field=models.IntegerField(),
        ),
    ]
