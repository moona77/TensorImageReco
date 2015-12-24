# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('netgraph', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 12, 23, 6, 19, 17, 126748, tzinfo=utc), max_length=100, help_text='Name used in URLs and file names.', unique=True, verbose_name='URL slug'),
            preserve_default=False,
        ),
    ]
