# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0007_auto_20160125_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsdata',
            name='Media',
            field=models.CharField(default=datetime.datetime(2016, 1, 25, 6, 38, 31, 291711, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
