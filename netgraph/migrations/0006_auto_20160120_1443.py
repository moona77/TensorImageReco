# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0005_auto_20160120_1424'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsdata',
            options={'ordering': ('Title',), 'verbose_name': 'New'},
        ),
        migrations.AlterField(
            model_name='newsdata',
            name='Url',
            field=models.URLField(unique=True, verbose_name='URL', db_index=True),
        ),
    ]
